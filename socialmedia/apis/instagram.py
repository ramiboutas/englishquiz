from __future__ import annotations

import json

import requests
from django.conf import settings

from socialmedia.models import InstagramPost


class AbractInstagramAPI:
    """
    Common shared data  & methods
    """

    def __init__(self) -> None:
        self.ig_user_id = settings.INSTAGRAM_PAGE_ID
        self.params = {"access_token": settings.INSTAGRAM_ACCESS_TOKEN}


class InstagramAPI(AbractInstagramAPI):
    def __init__(self) -> None:
        # do more here stuff if needed
        super().__init__()

    def create_post(self, text, image_url):
        # https://developers.facebook.com/docs/instagram-api/guides/content-publishing#paso-1-de-2--crear-contenedor

        self.params["caption"] = "testing caption..."
        self.params["image_url"] = "https://bit.ly/3fTIdet"  # This is an image

        response = requests.post(
            f"https://graph.facebook.com/v2.0/{self.ig_user_id}/media",
            params=self.params,
        )
        return response
        return InstagramPost.objects.create(
            instagram_id=json.loads(response.text)["id"], text=text
        )

    def delete_post(self, obj):
        pass
