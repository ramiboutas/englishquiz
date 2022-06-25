import random
import requests
import telegram
import tweepy

from django.conf import settings

from celery import shared_task

from quiz.models import Quiz, Lection
from utils.management import send_mail_to_admin

# If a post intent fails > notify the admin
# NEED TO SET UP EMAIL BACKEND FIRST
# extra_subject = 'Linkedin promotion FAILED'
# body_text = f'Response is not 201: {instance.full_url} \n {response}'
# send_mail_to_admin(extra_subject=extra_subject, body_text=body_text)


# General functions

def escape_html_for_telegram(text):
    text.replace("<", "&lt;")
    text.replace(">", "&gt;")
    text.replace("&", "&amp;")
    return text

def get_hashtag_str_from_post_instance_tags(instance):
    hashtag_str = ''
    for tag in instance.tags.all():
        hashtag_str += '#'+tag.name + ' '
    return hashtag_str


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


def post_text_in_linkedin(text):
    # scope: w_member_social,r_liteprofile
    profile_id = settings.LINKEDIN_PROFILE_ID
    access_token = settings.LINKEDIN_ACCESS_TOKEN

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}

    post_data = {
        "author": "urn:li:person:"+profile_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
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
def promote_post_instance_in_telegram(self, instance):
    try:
        hashtag_str = get_hashtag_str_from_post_instance_tags(instance)
        parsed_text = escape_html_for_telegram(f'{instance.title} \n👉 {instance.full_url} \n \n {hashtag_str}')
        post_text_in_telegram(text)

    except Exception as e:
        pass


@shared_task(bind=True)
def promote_post_instance_in_linkedin(self, instance):
    try:
        hashtag_str = get_hashtag_str_from_post_instance_tags(instance)
        text = f'{instance.title} \n👉 {instance.full_url} \n \n {hashtag_str}'
        response = post_text_in_linkedin(text)

        if not response.status_code == 201:
            pass

    except Exception as e:
        pass


@shared_task(bind=True)
def promote_post_instance_in_twitter(self, instance):
    try:
        hashtag_str = get_hashtag_str_from_post_instance_tags(instance)
        text = f'{instance.title} \n👉 {instance.full_url} \n \n {hashtag_str}'
        post_text_in_twitter(text)

    except Exception as e:
        pass



# Quiz tasks
@shared_task(bind=True)
def promote_quiz_instance_in_telegram(self, **kwargs):
    try:
        instance = Quiz.objects.get(pk=kwargs["pk"])
        text = f'🧑‍🏫 New quiz: {instance.name} \n \n👉 englishstuff.online{instance.get_detail_url()} \n \n #english #learnenglish #{instance.name.replace(" ", "")}'
        post_text_in_telegram(text)
        instance.promote = False
        instance.save()

    except Exception as e:
        pass


@shared_task(bind=True)
def promote_quiz_instance_in_linkedin(self, **kwargs):
    try:
        instance = Quiz.objects.get(pk=kwargs["pk"])
        text = f'🧑‍🏫 New quiz: {instance.name} \n \n👉 englishstuff.online{instance.get_detail_url()} \n \n Follow the linkedin page: https://www.linkedin.com/company/english-stuff-online/ \n \n  #english #learnenglish #{instance.name.replace(" ", "")}'
        response = post_text_in_linkedin(text)
        instance.promote = False
        instance.save()

        if not response.status_code == 201:
            pass

    except Exception as e:
        pass


@shared_task(bind=True)
def promote_quiz_instance_in_twitter(self, **kwargs):
    try:
        instance = Quiz.objects.get(pk=kwargs["pk"])
        text = f'🧑‍🏫 New quiz: {instance.name} \n \n👉 englishstuff.online{instance.get_detail_url()} \n \n #english #learnenglish #{instance.name.replace(" ", "")}'
        post_text_in_twitter(text)
        instance.promote = False
        instance.save()

    except Exception as e:
        pass

# Lection tasks

def get_salutation_text():
    salutation_options = ["Hey there!", "Hey, how is it going?", "Hi!", "Hey!", "Hey, what's up?"]
    return random.choice(salutation_options)


def get_question_text(instance):
    text = ""
    if instance.type == 1 or instance.type == 5:
        salutation_options = ["Hey there!", "Hey, how is it going?", "Hi!", "Hey!", "Hey, what's up?"]
        text += f"{random.choice(salutation_options)} \n\n"
    if instance.type == 1:
        text += f"📚 What do you think that comes in the gap? 🤔\n\n"
        text += f"{instance.text_one} ____ {instance.text_two}"
        if instance.text_three:
            text += f" ____ {instance.text_three}\n"
    if instance.type == 5:
        text += f"📚 What do you think is the right answer? 🤔\n\n"
        text += f"{instance.text_one}\n\n"
        text += f"💡 Options:\n"
        for answer in instance.answer_set.all():
            text += f" - {answer.name}\n"

    return text


@shared_task(bind=True)
def promote_lection_instance_in_telegram(self, **kwargs):
    try:
        instance = Lection.objects.get(pk=kwargs["pk"])
        question_text = get_question_text(instance.get_first_question())
        salutation_text = get_salutation_text()
        text = f"{salutation_text} \n\n"
        text += f'{question_text} \n\n'
        text += f'Check out the right answer here:\n'
        text += f'👉 englishstuff.online{instance.get_absolute_url()} \n \n'
        text += f'#english #learnenglish #{instance.name.replace(" ", "")}'
        post_text_in_telegram(text)
        if instance.promote:
            instance.promote = False
            instance.save()
    except Exception as e:
        raise e


@shared_task(bind=True)
def promote_lection_instance_in_linkedin(self, **kwargs):
    try:
        instance = Lection.objects.get(pk=kwargs["pk"])
        question_text = get_question_text(instance.get_first_question())
        salutation_text = get_salutation_text()
        text = f"{salutation_text} \n\n"
        text += f'{question_text} \n\n'
        text += f'Check out the right answer here:\n'
        text += f'👉 englishstuff.online{instance.get_absolute_url()} \n \n'
        text += f'#english #learnenglish #{instance.name.replace(" ", "")}'
        post_text_in_linkedin(text)
        if instance.promote:
            instance.promote = False
            instance.save()

    except Exception as e:
        raise e


@shared_task(bind=True)
def promote_lection_instance_in_twitter(self, **kwargs):
    try:
        instance = Lection.objects.get(pk=kwargs["pk"])
        question_text = get_question_text(instance.get_first_question())
        text = f'{question_text} \n\n'
        text += f'Check the answer:\n'
        text += f'👉 englishstuff.online{instance.get_absolute_url()} \n'
        text += f'#english #learnenglish'
        post_text_in_twitter(text)

        if instance.promote:
            instance.promote = False
            instance.save()

    except Exception as e:
        raise e
