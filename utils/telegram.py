import requests

import urllib.parse
import urllib.request

from django.conf import settings

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

bot = getattr(settings, "TELEGRAM_BOT_API_KEY", None)

if bot is None:
    raise Exception("settings.TELEGRAM_BOT_API_KEY is not set")


def make_request(endpoint: str, parameters: dict):
    data = urllib.parse.urlencode(parameters)
    data = data.encode("ascii")  # data should be bytes
    request = urllib.request.Request(endpoint, data)
    with urllib.request.urlopen(request) as response:
        return response


def report_to_admin(text: str):
    chat_id = settings.TELEGRAM_REPORTING_CHAT_ID
    send_message_to_telegram_chat(chat_id=chat_id, text=text)


def send_message_to_telegram_chat(text: str):
    base_url = f"https://api.telegram.org/bot{bot}/sendMessage"
    parameters = {"chat_id": settings.TELEGRAM_CHANNEL_NAME, "text": text}
    make_request(endpoint=base_url, parameters=parameters)


def send_image_to_telegram_chat(caption: str, image_url):
    base_url = f"https://api.telegram.org/bot{bot}/sendPhoto"
    parameters = {
        "chat_id": settings.TELEGRAM_CHANNEL_NAME,
        "caption": caption,
        "photo": image_url,
    }
    make_request(endpoint=base_url, parameters=parameters)
