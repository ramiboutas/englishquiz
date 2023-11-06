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

from utils.telegram import (
    report_to_admin,
    send_telegram_message,
    send_telegram_image,
)


@huey.db_periodic_task(crontab(month="2,4,6,8,10,12", day="29", hour="11", minute="19"))
def update_linkedin_access_token():
    try:
        update_access_token()
    except Exception as e:
        raise e


@huey.db_periodic_task(crontab(day="6", hour="9", minute="00"))
def share_random_book():
    book = Book.get_random_object_to_promote()
    text = book.get_promotion_text()
    try:
        # Linkedin
        li_post = LiPost.objects.create(comment=text, image=book.image)
        li_post.upload_image()
        li_post.share()

        # Telegram
        send_telegram_image(text, book.image.url)
        report_to_admin(f"Book promoted (id={book.id}):\n\n{text}")
    except Exception as e:
        report_to_admin(f"Error by promoting social post (id={book.id}):\n\n{e}")

    finally:
        # Setting field promoted to True -> so the social post cannot be reshared
        book.promoted = True
        book.save()


@huey.db_periodic_task(crontab(hour="11,13", minute="00"))
def share_random_quiz_question():
    question = Question.get_random_object_to_promote()
    text = question.get_question_promotion_text()
    try:
        # Telegram
        send_telegram_message(text)

        # Linkedin
        li_post = LiPost.objects.create(comment=text)
        li_post.share()

        # Twitter
        # if text.__len__() < 280:
        #    tweet = Tweet.objects.create(text=text)
        #    tweet.publish()

        report_to_admin(f"Quiz question promoted (id={question.id}):\n\n{text}")

    except Exception as e:
        report_to_admin(f"Error by promoting social post (id={question.id}):\n\n{e}")

    finally:
        # Setting field promoted to True -> so the social post cannot be reshared
        question.promoted = True
        question.save()


@huey.db_periodic_task(crontab(hour="15", minute="00"))
def share_random_quiz_question_as_poll():
    qs = Question.objects.filter(type=5)
    obj = random.choice(list(qs))
    question_text = obj.full_text
    options = obj.get_answer_list()
    text = obj.get_poll_explanation_text()

    # Linkedin
    # TODO: use LiPost or Poll (create in django-linkedin-posts)
    LinkedinPostAPI().create_poll(text, question_text=question_text, options=options)

    report_to_admin(f"Quiz question as poll promoted (id={obj.id}):\n\n{text}")


@huey.db_periodic_task(crontab(hour="8", minute="00"))
def share_social_post():
    """Share a random social post"""

    post = SocialPost.get_random_object_to_promote()
    try:
        # Telegram
        if post.promote_in_telegram:
            send_telegram_message(post.text)

        # Linkedin
        if post.promote_in_linkedin:
            li_post = LiPost.objects.create(comment=post.text)
            li_post.share()

        # Twitter
        # if post.promote_in_twitter and post.text.__len__() < 280:
        #     tweet = Tweet.objects.create(text=post.text)
        #     if post.file is not None:
        #         tweet_file = TweetFile.objects.create(file=post.file)
        #         uploaded_tweet_file = tweet_file.upload()
        #         tweet.files.add(uploaded_tweet_file)
        #     tweet.publish()
        report_to_admin(f"Social post promoted (id={post.id}):\n\n{post.text}")

    except Exception as e:
        report_to_admin(f"Error by promoting social post (id={post.id}):\n\n{e}")

    finally:
        # Setting field promoted to True -> so the social post cannot be reshared
        post.promoted = True
        post.save()


@huey.db_periodic_task(crontab(day="1", hour="9", minute="30"))
def share_blog_post():
    """Sharing a blog post in social media"""
    # Getting blog post
    post = BlogPost.get_random_object_to_promote()
    text = post.get_promotion_text()

    try:
        # Telegram
        send_telegram_message(text)

        # Linkedin
        li_post = LiPost.objects.create(comment=text)
        li_post.share()

        # Twitter
        # if text.__len__() < 280:
        #     tweet = Tweet.objects.create(text=text)
        #     tweet.publish()

        report_to_admin(f"Blog post promoted (id={post.id}):\n\n{text}")
    except Exception as e:
        report_to_admin(f"Error by promoting blog post (id={post.id}):\n\n{e}")

    finally:
        # Setting field promoted to True -> so the question cannot be reshared
        post.promoted = True
        post.save()
