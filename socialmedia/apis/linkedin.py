from __future__ import annotations

import json
import os
import time
import urllib.parse

import dotenv
import requests
from django.conf import settings


def update_access_token():
    # https://docs.microsoft.com/en-us/linkedin/shared/authentication/programmatic-refresh-tokens?view=li-lms-2022-06
    access_token = settings.LINKEDIN_ACCESS_TOKEN
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    post_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    post_data = {
        "refresh_token": settings.LINKEDIN_REFRESH_TOKEN,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET,
        "grant_type": "refresh_token",
    }

    response = requests.post(url, headers=post_headers, data=post_data)
    response = json.loads(response.text)
    access_token = response["access_token"]

    # update .env file
    # https://stackoverflow.com/questions/63837315/change-environment-variables-saved-in-env-file-with-python-and-dotenv
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    os.environ["LINKEDIN_ACCESS_TOKEN"] = access_token

    # Write changes to .env file.
    dotenv.set_key(
        dotenv_file,
        "LINKEDIN_ACCESS_TOKEN",
        os.environ["LINKEDIN_ACCESS_TOKEN"],
    )


class LinkedinPostAPI:
    def __init__(self, *args, **kwargs):
        self.access_token = settings.LINKEDIN_ACCESS_TOKEN
        self.organization_id = settings.LINKEDIN_AUTHOR_ID
        self.image_asset = None
        self.post_data = {
            "author": "urn:li:organization:" + self.organization_id,
            "commentary": "",
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }

        self.headers = {
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": "202211",
            "Authorization": "Bearer " + self.access_token,
        }

    def _add_text(self, text):
        self.post_data["commentary"] = text

    def _add_media(self, file_bytes):
        if file_bytes:
            image_asset = self.upload_image(file_bytes)
            self.post_data["content"] = {
                "media": {"title": "File from englishstuff.online", "id": image_asset}
            }
            self.image_asset = image_asset

    def _escape_text(self, text):
        chars = [
            ",",
            "{",
            "}",
            "@",
            "[",
            "]",
            "(",
            ")",
            "<",
            ">",
            "#",
            "",
            "*",
            "_",
            "~",
        ]
        for char in chars:
            text.replace(char, "\\" + char)
        return text

    def create_post(self, text: str, file_bytes: bytes = None):
        url = "https://api.linkedin.com/rest/posts"
        text = self._escape_text(text)
        self._add_text(text)
        self._add_media(file_bytes)
        response = requests.post(url, headers=self.headers, json=self.post_data)

    def create_poll(
        self, text: str, question_text: str = None, options: list[str] = None
    ):
        url = "https://api.linkedin.com/rest/posts"
        if question_text is None or options is None:
            return
        self._add_text(text)
        self.post_data["content"] = {
            "poll": {
                "question": question_text,
                "options": [{"text": option} for option in options],
                "settings": {"duration": "THREE_DAYS"},
            }
        }
        response = requests.post(url, headers=self.headers, json=self.post_data)
        return response

    def upload_image(self, file_bytes: bytes):
        upload_url, image_asset = self._initilize_image_upload()
        put_headers = {"Authorization": "Bearer " + self.access_token}
        requests.put(upload_url, headers=put_headers, data=file_bytes)

        completed = self.image_upload_completed(image_asset)
        passed_time = 0
        while not completed and passed_time < 20:
            time.sleep(1)
            passed_time += 1
            completed = self.image_upload_completed(image_asset)
        return image_asset

    def image_upload_completed(self, image_asset: str):
        response_dict = self.get_image(image_asset)
        if response_dict["status"] == "AVAILABLE":
            return True
        return False

    def get_image(self, image_asset: str):
        url = f"https://api.linkedin.com/rest/images/{urllib.parse.quote(image_asset)}"
        response = requests.get(url, headers=self.headers)
        data = json.loads(response.text)
        return data

    def _initilize_image_upload(self):
        url = "https://api.linkedin.com/rest/images?action=initializeUpload"
        post_data = {
            "initializeUploadRequest": {
                "owner": "urn:li:organization:" + self.organization_id
            }
        }
        response = requests.post(url, json=post_data, headers=self.headers)
        data = json.loads(response.text)
        upload_url = data["value"]["uploadUrl"]
        image_asset = data["value"]["image"]
        return upload_url, image_asset

    def delete_post(self, post_id: str):
        url = f"https://api.linkedin.com/rest/posts/{urllib.parse.quote(post_id)}"
        requests.delete(url, headers=self.headers)
