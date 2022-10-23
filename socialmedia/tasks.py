from __future__ import annotations

import random
import time
from io import BytesIO

from celery import shared_task
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont

from blog.models import BlogPost
from quiz.models import Question
from socialmedia.apis.linkedin import LinkedinCompanyPageAPI
from socialmedia.apis.telegram import TelegramAPI
from socialmedia.apis.twitter import TweetAPI
from socialmedia.models import RegularSocialPost, ScheduledSocialPost
from socialmedia.text import get_blog_post_promotion_text, get_question_promotion_text
from utils.mail import mail_admins_with_an_exception


# Image creation
def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = [""]
    for word in text.split(" "):
        line = f"{lines[-1]} {word}".strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return "\n".join(lines)


def create_image_from_instance(instance):
    text = instance.image_text
    font_size = 70
    text_color = (0, 90, 0)

    font_object = ImageFont.truetype("socialmedia/images/fonts/Georgia.ttf", font_size)
    blob = BytesIO()
    if instance.background_image_obj:
        imgObject = Image.open(instance.background_image_obj.image.file)
    else:
        imgObject = Image.open("socialmedia/images/default.jpg")
    width, height = imgObject.size
    height_offset = height * 0.35
    width_offset = width * 0.15

    for line_text in text.split("\n"):
        wrapped_line_text = get_wrapped_text(
            line_text, font_object, line_length=width - 2 * width_offset
        )
        number_of_produced_lines = len(wrapped_line_text.split("\n"))
        add_break_line = 0

        # add additional line if the line text is empty
        if line_text == "":
            add_break_line = font_size

        # draw on image
        drawing_object = ImageDraw.Draw(imgObject)
        drawing_object.multiline_text(
            (width_offset, height_offset),
            wrapped_line_text,
            font=font_object,
            fill=text_color,
        )
        # height_offset += font_object.getsize(wrapped_line_text)[1]*number_of_produced_lines + add_break_line
        height_offset += font_size * number_of_produced_lines + add_break_line

    if height_offset > height:
        # For large text, maybe implement...
        print("height_offset > height")
        print("Maybe inform programmer and do not create image")

    # imgObject.save('socialmedia/images/output/new_image.jpeg')
    imgObject.save(blob, "JPEG")
    instance.image.save(f"{instance.pk}".zfill(5) + ".jpg", File(blob), save=True)


@shared_task(bind=True)
def create_image_from_scheduled_social_post_instance(self, **kwargs):
    instance = ScheduledSocialPost.objects.get(pk=kwargs["pk"])
    create_image_from_instance(instance)


@shared_task(bind=True)
def create_image_from_regular_social_post_instance(self, **kwargs):
    instance = RegularSocialPost.objects.get(pk=kwargs["pk"])
    create_image_from_instance(instance)


# Linkedin update access token
@shared_task(bind=True)
def update_linkedin_company_page_access_token(self, **kwargs):
    try:
        LinkedinCompanyPageAPI().update_access_token()
    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e


#  Question promotion
@shared_task(bind=True)
def share_random_question_instance(self, **kwargs):
    try:
        # Getting random question
        questions = Question.objects.filter(promoted=False)

        if questions.exists():

            question = random.choice(list(questions))
            text = get_question_promotion_text(question)

            # Telegram
            TelegramAPI().send_message(text)

            # Linkedin
            LinkedinCompanyPageAPI().create_ugcPost(text)

            # Twitter
            if text.__len__() < 280:
                TweetAPI().create(text)

            # Facebook
            # FacebookPageAPI().create_post(text)
            # Instagram
            # TO DO

            # Setting field promoted to True -> so the question cannot be reshared
            question.promoted = True
            question.save()
        else:

            # TO DO: send email to admin: all questions were promoted!

            # Set all question instances to promoted=False
            Question.objects.all().update(promoted=False)

    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e


# Social posts


@shared_task(bind=True)
def promote_scheduled_social_post_instance(self, **kwargs):
    """
    Social post - triggered by post_save signal
    """
    time.sleep(
        10
    )  # for safety: in case we want to first create an image from the post instance
    try:
        instance = ScheduledSocialPost.objects.get(pk=kwargs["pk"])

        if instance.promote_in_telegram:
            TelegramAPI().send_message(instance.text)

        if instance.promote_in_linkedin:
            # LinkedinCompanyPageAPI().create_ugcPost(instance.text)
            LinkedinCompanyPageAPI().share_post_with_image(instance)

        if instance.text.__len__() < 280 and instance.promote_in_twitter:
            TweetAPI().create(instance.text)

        # if instance.promote_in_facebook:
        #     FacebookPageAPI().create_post(instance.text)

        # Instagram
        # TO DO

    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e


@shared_task(bind=True)
def share_regular_social_post(self, **kwargs):
    """
    Regular social post - triggered by celery beat (periodic task)
    """
    time.sleep(
        10
    )  # for safety: in case we want to first create an image from the post instance
    try:
        # Getting random social post
        social_posts = RegularSocialPost.objects.filter(promoted=False)

        if social_posts.exists():

            instance = random.choice(list(social_posts))

            # sharing

            if instance.promote_in_telegram:
                TelegramAPI().send_message(instance.text)

            if instance.promote_in_linkedin:
                LinkedinCompanyPageAPI().create_ugcPost(instance.text)

            if instance.promote_in_twitter and instance.text.__len__() < 280:
                TweetAPI().create(instance.text)

            # if instance.promote_in_facebook:
            #     FacebookPageAPI().create_post(instance.text)

            # Instagram
            # TO DO

            # Setting field promoted to True -> so the social post cannot be reshared
            instance.promoted = True
            instance.save()

        else:
            # TO DO: send email to admin: all regular social post objects were promoted!

            # Set all the regular social post objects to promoted = False
            RegularSocialPost.objects.all().update(promoted=False)

    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e


@shared_task(bind=True)
def share_regular_blog_post(self, **kwargs):
    """
    Regular social post - triggered by celery beat (periodic task)
    """
    try:
        # Getting blog post
        posts = BlogPost.objects.filter(promoted=False)

        if posts.exists():

            instance = random.choice(list(posts))

            text = get_blog_post_promotion_text(instance)

            # Telegram
            TelegramAPI().send_message(text)

            # Linkedin
            LinkedinCompanyPageAPI().create_ugcPost(text)

            # Twitter
            if text.__len__() < 280:
                TweetAPI().create(text)

            # Facebook
            # FacebookPageAPI().create_post(text)
            # Instagram
            # TO DO

            # Setting field promoted to True -> so the question cannot be reshared
            instance.promoted = True
            instance.save()
        else:

            # TO DO: send email to admin: all blog posts were promoted!

            # Set all blog posts¡ instances to promoted=False
            BlogPost.objects.all().update(promoted=False)

    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e
