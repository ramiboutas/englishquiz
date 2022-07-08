from time import sleep
import random
import requests
import telegram
import tweepy

from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

from puput.models import EntryPage
from quiz.models import Quiz, Lection, Question
from utils.management import send_mail_to_admin
from .models import ScheduledSocialPost, RegularSocialPost

from .text import get_question_promotion_text, escape_html_for_telegram, get_blog_post_promotion_text

# If a post intent fails > notify the admin
# NEED TO SET UP EMAIL BACKEND FIRST
# extra_subject = 'Linkedin promotion FAILED'
# body_text = f'Response is not 201: {instance.full_url} \n {response}'
# send_mail_to_admin(extra_subject=extra_subject, body_text=body_text)

# General variables and functions




logger = get_task_logger(__name__)




def post_text_in_twitter(text):
    # API keys
    api_key = settings.TWITTER_API_KEY
    api_secret = settings.TWITTER_API_KEY_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key,api_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Tweet intent
    api.update_status(status=text)


def post_text_in_telegram(text):
    parsed_text = escape_html_for_telegram(text)
    telegram_account = settings.TELEGRAM_ACCOUNT
    api_key = telegram_account["BOT_API_KEY"]
    channel = telegram_account["CHANNEL_NAME"]
    bot = telegram.Bot(token=api_key)
    bot.send_message(chat_id=channel, text=parsed_text,
        parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=False)




def post_text_in_linkedin_company_ugcPosts(text):
    organization_id = settings.LINKEDIN_ORGANIZATION_ID
    access_token = settings.LINKEDIN_ORGANIZATION_ACCESS_TOKEN

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}

    post_data = {
        "author": "urn:li:organization:"+organization_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
          "com.linkedin.ugc.ShareContent": {
           "shareMediaCategory": "NONE",
           "shareCommentary":{
            "text": text
           },
           "media": [],
           "shareCategorization": {}
          }
         },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=post_data)

    return response


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
            parsed_text = escape_html_for_telegram(text)
            post_text_in_telegram(parsed_text)

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
