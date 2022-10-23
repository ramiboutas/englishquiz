from __future__ import annotations

import json

import requests
from django.conf import settings

from socialmedia.models import FacebookPost


class AbstractFacebookPageAPI:
    """
    Common shared data  & methods
    """

    def __init__(self) -> None:
        self.page_id = settings.FACEBOOK_PAGE_ID
        self.params = {"access_token": settings.FACEBOOK_PAGE_ACCESS_TOKEN}

    def get_access_token(self):
        """
        It is not tested
        """
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET_KEY,
            "fb_exchange_token": settings.FACEBOOK_PAGE_ACCESS_TOKEN,
        }
        response = requests.get(
            "https://graph.facebook.com/oauth/access_token", params=params
        )
        # return response
        text_dict = json.loads(response.text)
        new_access_token = text_dict["access_token"]
        return new_access_token


class FacebookPageAPI(AbstractFacebookPageAPI):
    def __init__(self) -> None:
        # do more here stuff if needed
        super().__init__()

    def create_post(self, text):
        # curl -i -X POST "https://graph.facebook.com/{page-id}/feed
        # ?message=Hello Fans!&access_token={page-access-token}"
        self.params["message"] = text
        response = requests.post(
            f"https://graph.facebook.com/{self.page_id}/feed", params=self.params
        )
        return FacebookPost.objects.create(
            facebook_id=json.loads(response.text)["id"], text=text
        )

    def delete_post(self, obj):
        # curl -i -X DELETE "https://graph.facebook.com/{page-post-id}?access_token={page-access-token}"
        requests.delete(
            f"https://graph.facebook.com/{obj.facebook_id}", params=self.params
        )
