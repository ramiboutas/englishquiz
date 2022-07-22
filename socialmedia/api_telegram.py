import telegram

from django.conf import settings

from .models import TelegramMessage


class TelegramAPI:
    def __init__(self) -> None:
        self.channel = settings.TELEGRAM_CHANNEL_NAME
        self.bot = telegram.Bot(token=settings.TELEGRAM_BOT_API_KEY)
    
    def send_message(self, text):
        response = self.bot.send_message(chat_id=self.channel,
                                text=text,
                                parse_mode=telegram.ParseMode.HTML,
                                disable_web_page_preview=False
                            )
        
        try: 
            return TelegramMessage.objects.create(
                chat_id     = response.chat_id,
                message_id  = response.message_id,
                link        = response.link,
                text        = response.text,
                date        = response.date,
            )
        except:
            # THIS FAILS ON PRODUCTION -> psycopg2.errors.NumericValueOutOfRange: integer out of range
            # FIX ISSUE AND REMOVE THE DUMMY try/except
            pass

    def delete_message(self, telegram_obj):
        self.bot.delete_message(telegram_obj.chat_id, telegram_obj.message_id)
    



# animation
# audio
# author_signature
# bot
# caption
# caption_entities
# caption_html
# caption_html_urled
# caption_markdown
# caption_markdown_urled
# caption_markdown_v2
# caption_markdown_v2_urled
# channel_chat_created
# chat
# chat_id
# connected_website
# contact
# copy
# date
# de_json
# de_list
# delete
# delete_chat_photo
# dice
# document
# edit_caption
# edit_date
# edit_live_location
# edit_media
# edit_reply_markup
# edit_text
# effective_attachment
# entities
# forward
# forward_date
# forward_from
# forward_from_chat
# forward_from_message_id
# forward_sender_name
# forward_signature
# from_user
# game
# get_game_high_scores
# group_chat_created
# has_protected_content
# invoice
# is_automatic_forward
# left_chat_member
# link
# location
# media_group_id
# message_auto_delete_timer_changed
# message_id
# migrate_from_chat_id
# migrate_to_chat_id
# new_chat_members
# new_chat_photo
# new_chat_title
# parse_caption_entities
# parse_caption_entity
# parse_entities
# parse_entity
# passport_data
# photo
# pin
# pinned_message
# poll
# proximity_alert_triggered
# reply_animation
# reply_audio
# reply_chat_action
# reply_contact
# reply_copy
# reply_dice
# reply_document
# reply_game
# reply_html
# reply_invoice
# reply_location
# reply_markdown
# reply_markdown_v2
# reply_markup
# reply_media_group
# reply_photo
# reply_poll
# reply_sticker
# reply_text
# reply_to_message
# reply_venue
# reply_video
# reply_video_note
# reply_voice
# sender_chat
# set_game_score
# sticker
# stop_live_location
# stop_poll
# successful_payment
# supergroup_chat_created
# text
# text_html
# text_html_urled
# text_markdown
# text_markdown_urled
# text_markdown_v2
# text_markdown_v2_urled
# to_dict
# to_json
# unpin
# venue
# via_bot
# video
# video_chat_ended
# video_chat_participants_invited
# video_chat_scheduled
# video_chat_started
# video_note
# voice
# voice_chat_ended
# voice_chat_participants_invited
# voice_chat_scheduled
# voice_chat_started
# web_app_data