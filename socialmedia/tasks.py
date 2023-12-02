from __future__ import annotations

import random

from huey import crontab
from huey.contrib import djhuey as huey

from affiliates.models import Book
from blog.models import BlogPost
from quiz.models import Question
from socialmedia.apis.linkedin import LinkedinPostAPI
from socialmedia.apis.linkedin import update_access_token

from socialmedia.models import SocialPost

from django_tweets.models import Tweet
from django_tweets.models import TweetFile
from django_linkedin_posts.models import Post as LiPost
from django_linkedin_posts.models import Comment as LiComment
from django_linkedin_posts.models import create_poll_with_options


from utils.telegram import (
    report_to_admin,
    send_telegram_message,
    send_telegram_image,
)

QUESTION_AS_POLL_CRON_HOURS = "10"
QUESTION_CRON_HOURS = "14"
SOCIALPOST_CRON_HOURS = "16"


@huey.db_periodic_task(crontab(hour=QUESTION_CRON_HOURS, minute="00"))
def share_random_quiz_question():
    obj = random.choice(list(Question.objects.filter(promoted=False)))
    text = obj.get_question_promotion_text(add_link=False)
    text_with_link = obj.get_question_promotion_text(add_link=True)
    try:
        # Telegram
        send_telegram_message(text_with_link)

        # Linkedin
        li_post = LiPost.objects.create(text=text)
        li_post.share()
        obj.linkedin_post = li_post

        # Twitter
        # if text.__len__() < 280:
        #    tweet = Tweet.objects.create(text=text)
        #    tweet.publish()

        report_to_admin(f"Quiz question promoted (id={obj.id})")

    except Exception as e:
        report_to_admin(f"Error by promoting random question (id={obj.id}):\n\n{e}")
    else:
        # Setting field promoted to True -> so the social post cannot be reshared
        obj.promoted = True
        obj.save()


@huey.db_periodic_task(crontab(hour=QUESTION_AS_POLL_CRON_HOURS, minute="15"))
def share_random_quiz_question_as_poll():
    obj = random.choice(list(Question.objects.filter(type=5)))  # TODO: create a method!
    options = obj.get_answer_list()
    comment = obj.get_poll_explanation_text(add_link=False)
    question = obj.full_text
    # Linkedin
    poll = create_poll_with_options(comment, question, options, duration="ONE_DAY")
    try:
        poll.share()
        obj.linkedin_poll = poll
        obj.save()
        report_to_admin(f"Quiz question as poll promoted (id={obj.id})")
    except Exception as e:
        report_to_admin(f"Error by promoting poll (id={obj.id}):\n\n{e}")


@huey.db_periodic_task(crontab(day_of_week="2,6", hour="21", minute="25"))
def comment_linkedin_polls_with_correct_answer():
    questions = Question.objects.filter(
        linkedin_poll__isnull=False, linkedin_poll_commented=False
    )
    for question in questions:
        c = LiComment.objects.create(
            poll=question.linkedin_poll,
            text=question.post_comment_with_right_answer(),
        )
        c.share()
        question.linkedin_poll_commented = True
        question.save()


@huey.db_periodic_task(crontab(day_of_week="1,5", hour="21", minute="25"))
def comment_linkedin_posts_with_correct_answer():
    questions = Question.objects.filter(
        linkedin_post__isnull=False, linkedin_post_commented=False
    )
    for question in questions:
        c = LiComment.objects.create(
            post=question.linkedin_post,
            text=question.post_comment_with_right_answer(),
        )
        c.share()
        question.linkedin_post_commented = True
        question.save()


@huey.db_periodic_task(crontab(hour=SOCIALPOST_CRON_HOURS, minute="30"))
def share_social_post():
    """Share a random social post"""

    obj = SocialPost.get_random_object_to_promote()
    try:
        # Telegram
        if obj.promote_in_telegram:
            send_telegram_message(obj.text)

        # Linkedin
        if obj.promote_in_linkedin:
            li_post = LiPost.objects.create(text=obj.text)
            li_post.share()

        # Twitter
        # if post.promote_in_twitter and post.text.__len__() < 280:
        #     tweet = Tweet.objects.create(text=post.text)
        #     if post.file is not None:
        #         tweet_file = TweetFile.objects.create(file=post.file)
        #         uploaded_tweet_file = tweet_file.upload()
        #         tweet.files.add(uploaded_tweet_file)
        #     tweet.publish()
        report_to_admin(f"Social post promoted (id={obj.id})")

    except Exception as e:
        report_to_admin(f"Error by promoting social post (id={obj.id}):\n\n{e}")

    finally:
        # Setting field promoted to True -> so the social post cannot be reshared
        obj.promoted = True
        obj.save()


@huey.db_periodic_task(crontab(day_of_week="2", hour="9", minute="40"))
def share_blog_post():
    """Sharing a blog post in social media"""
    # Getting blog post
    obj = BlogPost.get_random_object_to_promote()
    text = obj.get_promotion_text()

    try:
        # Telegram
        send_telegram_message(text)

        # Linkedin
        li_post = LiPost.objects.create(text=text)
        li_post.share()

        # Twitter
        # if text.__len__() < 280:
        #     tweet = Tweet.objects.create(text=text)
        #     tweet.publish()

        report_to_admin(f"Blog post promoted (id={obj.id}):\n\n{text}")
    except Exception as e:
        report_to_admin(f"Error by promoting blog post (id={obj.id}):\n\n{e}")

    finally:
        # Setting field promoted to True -> so the question cannot be reshared
        obj.promoted = True
        obj.save()


@huey.db_periodic_task(crontab(day_of_week="4", hour="9", minute="50"))
def share_random_book():
    obj = Book.get_random_object_to_promote()
    text = obj.get_promotion_text()
    try:
        # Linkedin
        li_post = LiPost.objects.create(text=text, image=obj.image)
        li_post.upload_image()
        li_post.share()

        # Telegram
        send_telegram_image(text, obj.image.url)
        report_to_admin(f"Book promoted (id={obj.id}):\n\n{text}")
    except Exception as e:
        report_to_admin(f"Error by promoting social post (id={obj.id}):\n\n{e}")

    finally:
        # Setting field promoted to True -> so the social post cannot be reshared
        obj.promoted = True
        obj.save()


@huey.db_periodic_task(crontab(month="2,4,6,8,10,12", day="29", hour="11", minute="10"))
def update_linkedin_access_token():
    try:
        update_access_token()
    except Exception as e:
        raise e
