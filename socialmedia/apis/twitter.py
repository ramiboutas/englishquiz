from __future__ import annotations

import tweepy
from django.conf import settings

from socialmedia.models import FavoriteTweetSearch
from socialmedia.models import Tweet


class AbtractTwiterAPI:
    def __init__(self) -> None:
        self.auth = tweepy.OAuthHandler(
            settings.TWITTER_API_KEY, settings.TWITTER_API_KEY_SECRET
        )
        self.auth.set_access_token(
            settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)


class TweetAPI(AbtractTwiterAPI):
    def create(self, text):
        """
        It creates a tweet and saves it in our database
        """
        response = self.api.update_status(status=text)
        return Tweet.objects.create(
            created_at=response.created_at,
            favorite_count=response.favorite_count,
            twitter_id=response.id,
            id_str=response.id_str,
            retweet_count=response.retweet_count,
            text=response.text,
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
        tweet_obj.favorite_count = response.favorite_count
        tweet_obj.retweet_count = response.retweet_count
        tweet_obj.text = response.text
        tweet_obj.save()

    def like_recent_tweets(self):
        searches = FavoriteTweetSearch.objects.all()
        for search in searches:
            tweet_list = tweepy.Cursor(
                self.api.search_tweets,
                search.name,
                lang=search.lang_code,
                result_type="recent",
            ).items(search.number_of_likes)

            for tweet in tweet_list:
                try:
                    tweet.favorite()
                except:
                    pass
