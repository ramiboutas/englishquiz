from __future__ import annotations

import telegram as telegram_bot
from django.conf import settings

from socialmedia.models import TelegramMessage


class TelegramAPI:
    def __init__(self) -> None:
        self.channel = settings.TELEGRAM_CHANNEL_NAME
        self.bot = telegram_bot.Bot(token=settings.TELEGRAM_BOT_API_KEY)

    def send_message(self, text):
        response = self.bot.send_message(
            chat_id=self.channel,
            text=text,
            parse_mode=telegram_bot.ParseMode.HTML,
            disable_web_page_preview=False,
        )

        return TelegramMessage.objects.create(
            chat_id=response.chat_id,
            message_id=response.message_id,
            link=response.link,
            text=response.text,
            date=response.date,
        )
    
    def send_poll(self, text:str, options:list[str]=None, explanation:str=None, correct_option_id:int=None):
        # TODO: fix:
        # TypeError(f'Object of type {o.__class__.__name__} ' 
        # TypeError: Object of type method is not JSON serializable
        
        self.bot.send_poll(
            chat_id=self.channel,
            question=text,
            options=options,
            explanation=explanation,
            correct_option_id=correct_option_id
        )

    def delete_message(self, telegram_obj):
        self.bot.delete_message(telegram_obj.chat_id, telegram_obj.message_id)
