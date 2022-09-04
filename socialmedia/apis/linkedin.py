import os
import time
import requests
import json
import urllib.parse
import dotenv

from django.conf import settings

from socialmedia.models import LinkedinPost

class AbractLinkedinCompanyPageAPI:
    """
    Common shared data  & methods
    """
    def __init__(self) -> None:
        access_token = settings.LINKEDIN_ORGANIZATION_ACCESS_TOKEN
        self.headers = {'Content-Type': 'application/json',
                        'X-Restli-Protocol-Version': '2.0.0',
                        'Authorization': 'Bearer ' + access_token}

    def update_access_token(self):
        # https://docs.microsoft.com/en-us/linkedin/shared/authentication/programmatic-refresh-tokens?view=li-lms-2022-06
        
        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        post_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        post_data = {
            'refresh_token': settings.LINKEDIN_ORGANIZATION_REFRESH_TOKEN,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET,
            'grant_type': 'refresh_token',
        }
        full_response_obj = requests.post(url, headers=post_headers, data=post_data)
        response =  json.loads(full_response_obj.text)
        access_token = response["access_token"]
        # update .env file
        # https://stackoverflow.com/questions/63837315/change-environment-variables-saved-in-env-file-with-python-and-dotenv
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        os.environ["LINKEDIN_ORGANIZATION_ACCESS_TOKEN"] = access_token
        # Write changes to .env file.
        dotenv.set_key(dotenv_file, "LINKEDIN_ORGANIZATION_ACCESS_TOKEN", os.environ["LINKEDIN_ORGANIZATION_ACCESS_TOKEN"])
    

class LinkedinCompanyPageAPI(AbractLinkedinCompanyPageAPI):
    def __init__(self) -> None:
        organization_id = settings.LINKEDIN_ORGANIZATION_ID
        self.post_data = {
            "author": "urn:li:organization:"+organization_id,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareMediaCategory": "NONE",
                    "shareCommentary":{},
                    "media": [],
                    "shareCategorization": {}
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }

        super().__init__()


    def create_ugcPost(self, text):
        url = "https://api.linkedin.com/v2/ugcPosts"
        self.post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"] = text
        response = requests.post(url, headers=self.headers, json=self.post_data)
        return LinkedinPost.objects.create(urn_li_share=json.loads(response.text)["id"], text=text)
        

    def delete_ugcPost(self, linkedinpost_obj):
        url = f'https://api.linkedin.com/v2/ugcPosts/{urllib.parse.quote(linkedinpost_obj.urn_li_share)}'
        requests.delete(url, headers=self.headers)


    def register_upload(self):
        url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        parameters = {
                "registerUploadRequest":{
                    "owner":"urn:li:organization:"+settings.LINKEDIN_ORGANIZATION_ID,
                    "recipes":[
                        "urn:li:digitalmediaRecipe:feedshare-image"
                    ],
                    "serviceRelationships":[
                        {
                            "identifier":"urn:li:userGeneratedContent",
                            "relationshipType":"OWNER"
                        }
                    ],
                    "supportedUploadMechanism":[
                        "SYNCHRONOUS_UPLOAD"
                    ]
                }
            }
        full_response_obj = requests.post(url, headers=self.headers, json=parameters)
        response =  json.loads(full_response_obj.text)
        upload_url = response["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        media_asset = response["value"]["asset"]
        return (upload_url, media_asset)
    
    def share_post_with_image(self, social_post_instance):
        upload_url, media_asset = self.register_upload()
        put_headers = {'Authorization': 'Bearer '+settings.LINKEDIN_ORGANIZATION_ACCESS_TOKEN,}

        # social_post_instance.image.file.path ??
        # with open('/home/rami/dev/github/englishquiz/media/socialposts/images/Image__3.jpg', 'rb') as f:
        #     put_data = f.read()
        
        put_data = social_post_instance.image.open('r').read()
        
        requests.put(upload_url, headers=put_headers, data=put_data)
        time.sleep(5)


        ugcPost_url = "https://api.linkedin.com/v2/ugcPosts"
        self.post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"] = social_post_instance.text
        self.post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
        self.post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                {
                    "media": media_asset,
                    "status": "READY",
                    "title": {
                        "attributes": [],
                        "text": "English Stuff Online | Practice with Quizzes"
                    }
                }
            ]
        
        
        response = requests.post(ugcPost_url, headers=self.headers, json=self.post_data)

        return LinkedinPost.objects.create(urn_li_share=json.loads(response.text)["id"], text=social_post_instance.text, media_asset=media_asset)




    