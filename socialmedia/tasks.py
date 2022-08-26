import random


from celery import shared_task

from utils.mail import mail_admins_with_an_exception
from .models import ScheduledSocialPost, RegularSocialPost
from quiz.models import Quiz, Lection, Question
from blog.models import BlogPost

from .text import get_question_promotion_text, get_blog_post_promotion_text

from .api_twitter import TweetAPI
from .api_telegram import TelegramAPI
from .api_linkedin import LinkedinCompanyPageAPI
from .api_facebook import FacebookPageAPI



#  Question promotion
@shared_task(bind=True)
def share_random_question_instance(self, **kwargs):
    try:
        # Getting random question
        questions = Question.objects.filter(promoted=False)
        
        if questions.exists():

            question = random.choice(list(questions))
            text = get_question_promotion_text(question)
            
            # Telegram
            TelegramAPI().send_message(text)
            
            # Linkedin
            LinkedinCompanyPageAPI().create_ugcPost(text)
            
            # Twitter
            if text.__len__() < 280:
                TweetAPI().create(text)
            
            # Facebook
            FacebookPageAPI().create_post(text)
            # Instagram
            # TO DO

            # Setting field promoted to True -> so the question cannot be reshared
            question.promoted = True
            question.save()
        else:
            
            # TO DO: send email to admin: all questions were promoted!

            # Set all question instances to promoted=False
            Question.objects.all().update(promoted=False)
            

    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e


# Social posts

@shared_task(bind=True)
def promote_scheduled_social_post_instance(self, **kwargs):
    """
    Social post - triggered by post_save signal
    """

    try:
        instance = ScheduledSocialPost.objects.get(pk=kwargs["pk"])
        
        if instance.promote_in_telegram:            
            TelegramAPI().send_message(instance.text)
        
        if instance.promote_in_linkedin:
            LinkedinCompanyPageAPI().create_ugcPost(instance.text)

        if instance.text.__len__() < 280 and instance.promote_in_twitter:
            TweetAPI().create(instance.text)
        
        if instance.promote_in_facebook:
            FacebookPageAPI().create_post(instance.text)
        
        # Instagram
            # TO DO

    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e


@shared_task(bind=True)
def share_regular_social_post(self, **kwargs):
    """
    Regular social post - triggered by celery beat (periodic task)
    """
    try:
        # Getting random social post
        social_posts = RegularSocialPost.objects.filter(promoted=False)

        if social_posts.exists():

            instance = random.choice(list(social_posts))
            
            # sharing

            if instance.promote_in_telegram:
                TelegramAPI().send_message(instance.text)
                
            if instance.promote_in_linkedin:
                LinkedinCompanyPageAPI().create_ugcPost(instance.text)

            if instance.promote_in_twitter and instance.text.__len__() < 280:
                TweetAPI().create(instance.text)
            
            if instance.promote_in_facebook:
                FacebookPageAPI().create_post(instance.text)
            
            # Instagram
            # TO DO

            # Setting field promoted to True -> so the social post cannot be reshared
            instance.promoted=True
            instance.save()

        else:
            # TO DO: send email to admin: all regular social post objects were promoted!

            # Set all the regular social post objects to promoted = False
            RegularSocialPost.objects.all().update(promoted=False)

    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e


@shared_task(bind=True)
def share_regular_blog_post(self, **kwargs):
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
            LinkedinCompanyPageAPI().create_ugcPost(text)
            
            # Twitter
            if text.__len__() < 280:
                TweetAPI().create(text)
            
            # Facebook
            FacebookPageAPI().create_post(text)
            # Instagram
            # TO DO

            # Setting field promoted to True -> so the question cannot be reshared
            instance.promoted = True
            instance.save()
        else:
            
            # TO DO: send email to admin: all blog posts were promoted!

            # Set all blog posts¡ instances to promoted=False
            BlogPost.objects.all().update(promoted=False)
            

    except Exception as e:
        mail_admins_with_an_exception(e)
        raise e