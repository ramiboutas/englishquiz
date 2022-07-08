import telegram

from django.conf import settings


def escape_html_for_telegram(text):
    text.replace("<", "&lt;")
    text.replace(">", "&gt;")
    text.replace("&", "&amp;")
    return text


def post_text_in_telegram(text):
    parsed_text = escape_html_for_telegram(text)
    telegram_account = settings.TELEGRAM_ACCOUNT
    api_key = telegram_account["BOT_API_KEY"]
    channel = telegram_account["CHANNEL_NAME"]
    bot = telegram.Bot(token=api_key)
    bot.send_message(chat_id=channel, text=parsed_text,
        parse_mode=telegram.ParseMode.HTML, disable_web_page_preview=False)