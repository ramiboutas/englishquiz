from urllib import response
import tweepy

from django.conf import settings



def post_text_in_twitter(text):
    # API keys
    api_key = settings.TWITTER_API_KEY
    api_secret = settings.TWITTER_API_KEY_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Tweet intent
    api.update_status(status=text)


from .models import Tweet

class AbtractTwiterAPI:
    def __init__(self) -> None:
        api_key        = settings.TWITTER_API_KEY
        api_secret     = settings.TWITTER_API_KEY_SECRET
        access_token   = settings.TWITTER_ACCESS_TOKEN
        access_secret  = settings.TWITTER_ACCESS_TOKEN_SECRET

        self.auth           = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(access_token, access_secret)
        self.api            = tweepy.API(self.auth, wait_on_rate_limit=True)



class TweetAPI(AbtractTwiterAPI):

    def create(self, text):
        """ 
        It creates a tweet and saves it in our database
        """
        response = self.api.update_status(status=text)
        self.id = response.id
        return Tweet.objects.create(
            created_at      = response.created_at,
            favorite_count  = response.favorite_count,
            twitter_id      = response.id,
            id_str          = response.id_str,
            retweet_count   = response.retweet_count,
            text            = response.text,
        )
        
        
    def delete(self, tweet_obj):
        """ 
        It deletes a tweet from twitter
        """
        self.api.destroy_status(id=tweet_obj.twitter_id)
    

    def get_status(self, tweet_obj):
        """ 
        It gets new info and updates the status of a tweet object
        """
        response = self.api.get_status(id=tweet_obj.twitter_id)
        tweet_obj.created_at      = response.created_at
        tweet_obj.favorite_count  = response.favorite_count
        tweet_obj.twitter_id      = response.id
        tweet_obj.id_str          = response.id_str
        tweet_obj.retweet_count   = response.retweet_count
        tweet_obj.text            = response.text
        tweet_obj.save()

