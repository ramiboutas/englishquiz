import random


from celery import shared_task
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

from puput.models import EntryPage

from utils.management import send_mail_to_admin
from .models import ScheduledSocialPost, RegularSocialPost
from quiz.models import Quiz, Lection, Question

from .text import get_question_promotion_text, get_blog_post_promotion_text
from .api_twitter import post_text_in_twitter
from .api_telegram import post_text_in_telegram
from .api_linkedin import post_text_in_linkedin_company_ugcPosts



# If a post intent fails > notify the admin
# NEED TO SET UP EMAIL BACKEND FIRST
# extra_subject = 'Linkedin promotion FAILED'
# body_text = f'Response is not 201: {instance.full_url} \n {response}'
# send_mail_to_admin(extra_subject=extra_subject, body_text=body_text)
# from django.core.mail import mail_admins
#  mail_admins(subject, message, fail_silently=False, connection=None, html_message=None)[source]¶

# General variables and functions


# Blog post tasks
@shared_task(bind=True)
def promote_blog_post_instance(self, **kwargs):
    """
    It promotes in social media a blog post instance
    """
    
    try: 
        instance = EntryPage.objects.get(pk=kwargs["pk"])
        text = get_blog_post_promotion_text(instance)

        if instance.promote_in_linkedin:    
            linkedin_response = post_text_in_linkedin_company_ugcPosts(text)
            # save LinkedPost instance 

        if instance.promote_in_telegram:
            post_text_in_telegram(text)

        if instance.promote_in_twitter:    
            twitter_response = post_text_in_twitter(text)
            # save the tweet? how?
    
    except Exception as e:
        raise e



#  Question tasks

@shared_task(bind=True)
def share_random_question_instance(self, **kwargs):
    try:
        # Getting random question
        questions = Question.objects.filter(promoted=False)
        question = random.choice(list(questions))

        text = get_question_promotion_text(question)

        if question:
            # sharing
            post_text_in_telegram(text)
            post_text_in_linkedin_company_ugcPosts(text)

            if text.__len__() < 280:
                post_text_in_twitter(text)

            # Setting field promoted to True -> so the question cannot be reshared
            question.promoted=True
            question.save()
        else:
            # Set all question instances to promoted=False
            if questions is not None:
                questions.update(promoted=False)

    except Exception as e:
        raise e


# Social posts

@shared_task(bind=True)
def promote_scheduled_social_post_instance(self, **kwargs):
    """
    Social post - triggered by post_save signal
    """
    try:
        instance = ScheduledSocialPost.objects.get(pk=kwargs["pk"])
        post_text_in_telegram(instance.text)
        post_text_in_linkedin_company_ugcPosts(instance.text)

        if instance.text.__len__() < 280:
            post_text_in_twitter(instance.text)

    except Exception as e:
        raise e


@shared_task(bind=True)
def share_regular_social_post(self, **kwargs):
    """
    Regular social post - triggered by celery beat (periodic task)
    """
    try:
        # Getting random social post
        social_posts = RegularSocialPost.objects.filter(promoted=False)
        instance = random.choice(list(social_posts))

        if instance:
            # sharing
            post_text_in_telegram(instance.text)
            post_text_in_linkedin_company_ugcPosts(instance.text)

            if instance.text.__len__() < 280:
                post_text_in_twitter(instance.text)
            # Setting field promoted to True -> so the social post cannot be reshared
            instance.promoted=True
            instance.save()

        else:
            if social_posts is not None:
                social_posts.update(promoted=False)

    except Exception as e:
        raise e
