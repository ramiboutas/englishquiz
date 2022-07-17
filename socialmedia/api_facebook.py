from os import access
import requests
import json
import urllib.parse

from django.conf import settings

from .models import FacebookPost

class AbractFacekookPageAPI:
    """
    Common shared data  & methods
    """
    def __init__(self) -> None:
        
        self.page_id = settings.FACEBOOK_PAGE_ID
        self.access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
        
        self.app_id = settings.FACEBOOK_APP_ID
        self.client_secret = settings.FACEBOOK_APP_SECRET_KEY

        self.headers = {'Content-Type': 'application/json'}
    
    def get_access_token(self):
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': self.app_id,
            'client_secret': self.client_secret,
            'fb_exchange_token': self.access_token,
        }
        response = requests.get('https://graph.facebook.com/oauth/access_token', params=params)
        return response 
        text_dict = json.loads(response.text)
        new_access_token = text_dict["access_token"]
        return new_access_token


class FacebookPageAPI(AbractFacekookPageAPI):
    def __init__(self) -> None:
        # do more here stuff if needed
        super().__init__()

    def create_post(self, text):
        # curl -i -X POST "https://graph.facebook.com/{page-id}/feed
        # ?message=Hello Fans!&access_token={page-access-token}"

        url = f"https://graph.facebook.com/{self.page_id}/feed"
        params = {'message': text, 'access_token': self.access_token}
        response = requests.post(url, params=params)
        return FacebookPost.objects.create(facebook_id = json.loads(response.text)["id"], text= text)

    def delete_post(self, facebookpost_obj):
        # curl -i -X DELETE "https://graph.facebook.com/{page-post-id}
        # ?access_token={page-access-token}"
        url = f"https://graph.facebook.com/{facebookpost_obj.facebook_id}"
        params = {'access_token': self.access_token}
        requests.delete(url, params=params)


