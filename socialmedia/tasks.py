from __future__ import annotations

import time
import random

from celery import shared_task

from blog.models import BlogPost
from quiz.models import Question
from socialmedia.apis.linkedin import LinkedinPostAPI
from socialmedia.apis.linkedin import update_access_token
from socialmedia.apis.telegram import TelegramAPI
from socialmedia.models import SocialPost
from socialmedia.text import get_blog_post_promotion_text
from socialmedia.text import get_poll_explanation_text
from socialmedia.text import get_question_promotion_text

from django_tweets.models import Tweet
from django_tweets.models import TweetFile


@shared_task(bind=True)
def update_linkedin_company_page_access_token(self, **kwargs):
    try:
        update_access_token()
    except Exception as e:
        raise e


@shared_task(bind=True)
def share_random_quiz_question(self, **kwargs):
    try:
        # Getting random question
        questions = Question.objects.filter(promoted=False)

        if questions.exists():
            question = random.choice(list(questions))
            text = get_question_promotion_text(question)

            # Telegram
            TelegramAPI().send_message(text)

            # Linkedin
            LinkedinPostAPI().create_post(text)

            # Twitter
            if text.__len__() < 280:
                tweet = Tweet.objects.create(text=text)
                tweet.publish()

            # Setting field promoted to True -> so the question cannot be reshared
            question.promoted = True
            question.save()
        else:
            # Set all question instances to promoted=False
            Question.objects.all().update(promoted=False)

    except Exception as e:
        raise e


@shared_task(bind=True)
def share_random_quiz_question_as_poll(self, **kwargs):
    qs = Question.objects.filter(type=5)
    obj = random.choice(list(qs))
    question_text = obj.full_text
    options = obj.get_answer_list()
    text = get_poll_explanation_text(obj)

    # Linkedin
    LinkedinPostAPI().create_poll(text, question_text=question_text, options=options)


@shared_task(bind=True)
def share_social_post(self, **kwargs):
    """
    Regular social post - triggered by celery beat (periodic task)
    """
    # for safety: in case we want to first create an image from the post instance
    time.sleep(10)

    try:
        # Getting random social post
        social_posts = SocialPost.objects.filter(promoted=False)

        if social_posts.exists():
            post = random.choice(list(social_posts))

            # sharing

            if post.promote_in_telegram:
                TelegramAPI().send_message(post.text)

            if post.promote_in_linkedin:
                LinkedinPostAPI().create_post(post.text)

            if post.promote_in_twitter and post.text.__len__() < 280:
                tweet = Tweet.objects.create(text=post.text)

                if post.file is not None:
                    tweet_file = TweetFile.objects.create(file=post.file)
                    uploaded_tweet_file = tweet_file.upload()
                    tweet.files.add(uploaded_tweet_file)
                tweet.publish()

            # Setting field promoted to True -> so the social post cannot be reshared
            post.promoted = True
            post.save()

        else:
            # Set all the regular social post objects to promoted = False
            SocialPost.objects.all().update(promoted=False)

    except Exception as e:
        raise e


@shared_task(bind=True)
def share_blog_post(self, **kwargs):
    """
    Regular social post - triggered by celery beat (periodic task)
    """
    try:
        # Getting blog post
        posts = BlogPost.objects.filter(promoted=False)

        if posts.exists():
            instance = random.choice(list(posts))

            text = get_blog_post_promotion_text(instance)

            # Telegram
            TelegramAPI().send_message(text)

            # Linkedin
            LinkedinPostAPI().create_post(text)

            # Twitter
            if text.__len__() < 280:
                tweet = Tweet.objects.create(text=text)
                tweet.publish()

            # Setting field promoted to True -> so the question cannot be reshared
            instance.promoted = True
            instance.save()
        else:
            # Set all blog posts¡ instances to promoted=False
            BlogPost.objects.all().update(promoted=False)

    except Exception as e:
        raise e
