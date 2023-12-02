import requests


from django.conf import settings

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

bot = getattr(settings, "TELEGRAM_BOT_API_KEY", None)

if bot is None:
    raise Exception("settings.TELEGRAM_BOT_API_KEY is not set")

default_chat = settings.TELEGRAM_CHANNEL_NAME


def report_to_admin(text: str):
    send_telegram_message(chat_id=settings.TELEGRAM_REPORTING_CHAT_ID, text=text)


def send_telegram_message(text: str, chat_id=default_chat):
    url = f"https://api.telegram.org/bot{bot}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    r = requests.get(url, data=data)
    return r.text


def send_telegram_image(caption: str, image_url, chat_id=default_chat):
    url = f"https://api.telegram.org/bot{bot}/sendPhoto"
    data = {"chat_id": chat_id, "caption": caption, "photo": image_url}
    r = requests.get(url, data=data)
    return r.text
