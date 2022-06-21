import requests
import telegram
import tweepy


from django.conf import settings

from celery import shared_task

from utils.management import send_mail_to_admin



def escape_html_for_telegram(text):
    text.replace("<", "&lt;")
    text.replace(">", "&gt;")
    text.replace("&", "&amp;")
    return text



@shared_task(bind=True)
def promote_post_instance_in_telegram(self, instance):
    try:

        parsed_text = "testing message"
        telegram_account = settings.TELEGRAM_ACCOUNT
        api_key = telegram_account["BOT_API_KEY"]
        channel = telegram_account["CHANNEL_NAME"]
        bot = telegram.Bot(token=api_key)
        bot.send_message(chat_id=channel, text=parsed_text,
            parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=False)

    except Exception as e:
        pass
        # NEED TO SET UP EMAIL BACKEND FIRST
        # extra_subject = 'Telegram promotion FAILED'
        # body_text = f'Exception occurred: {instance.full_url} \n {e}'
        # send_mail_to_admin(extra_subject=extra_subject, body_text=body_text)


@shared_task(bind=True)
def promote_post_instance_in_linkedin(self, instance):
    # scope: w_member_social,r_liteprofile
    try:
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
                        "text": f'New post available \n {instance.full_url} '
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(url, headers=headers, json=post_data)
        if not response.status_code == 201:
            pass
            # NEED TO SET UP EMAIL BACKEND FIRST
            # extra_subject = 'Linkedin promotion FAILED'
            # body_text = f'Response is not 201: {instance.full_url} \n {response}'
            # send_mail_to_admin(extra_subject=extra_subject, body_text=body_text)

    except Exception as e:
        pass
        # NEED TO SET UP EMAIL BACKEND FIRST
        # extra_subject = 'Linkedin promotion FAILED'
        # body_text = f'Exception occurred: {instance.full_url} \n {e}'
        # send_mail_to_admin(extra_subject=extra_subject, body_text=body_text)


@shared_task(bind=True)
def promote_post_instance_in_twitter(self, instance):
    try:
        # API keys
        api_key = settings.TWITTER_API_KEY
        api_secret = settings.TWITTER_API_KEY_SECRET
        access_token = settings.TWITTER_ACCESS_TOKEN
        access_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(api_key,api_secret)
        auth.set_access_token(access_token,access_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True)

        status = f"New post available \n {instance.full_url}"
        api.update_status(status=status)

    except Exception as e:
        pass
        # NEED TO SET UP EMAIL BACKEND FIRST
        # extra_subject = 'Twitter promotion FAILED'
        # body_text = f'{instance.full_url} \n {e}'
        # send_mail_to_admin(extra_subject=extra_subject, body_text=body_text)
