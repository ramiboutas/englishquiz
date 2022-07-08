import tweepy

from django.conf import settings

def post_text_in_twitter(text):
    # API keys
    api_key = settings.TWITTER_API_KEY
    api_secret = settings.TWITTER_API_KEY_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key,api_secret)
    auth.set_access_token(access_token,access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Tweet intent
    api.update_status(status=text)
