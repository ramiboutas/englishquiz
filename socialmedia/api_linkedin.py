import requests
import json
import urllib.parse

from django.conf import settings

from .models import LinkedinPost

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
        # figure out how to make modifications in .env file
        # https://stackoverflow.com/questions/43933897/set-environment-variables-by-file-using-python
        # https://stackoverflow.com/questions/63837315/change-environment-variables-saved-in-env-file-with-python-and-dotenv
        pass

        


class LinkedinCompanyPageAPI(AbractLinkedinCompanyPageAPI):
    def __init__(self) -> None:
        organization_id = settings.LINKEDIN_ORGANIZATION_ID
        self.post_data = {
            "author": "urn:li:organization:"+organization_id,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
            "com.linkedin.ugc.ShareContent": {
            "shareMediaCategory": "NONE",
            "shareCommentary":{
            },
            "media": [],
            "shareCategorization": {}
            }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        super().__init__()

    def create_ugcPost(self, text):
        url = "https://api.linkedin.com/v2/ugcPosts"
        self.post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareCommentary"]["text"] = text
        response = requests.post(url, headers=self.headers, json=self.post_data)
        return LinkedinPost.objects.create(urn_li_share  = json.loads(response.text)["id"], text= text)

    def delete_ugcPost(self, linkedinpost_obj):
        url = f'https://api.linkedin.com/v2/ugcPosts/{urllib.parse.quote(linkedinpost_obj.urn_li_share)}'
        requests.delete(url, headers=self.headers)








def post_text_in_linkedin_company_ugcPosts(text):
    organization_id = settings.LINKEDIN_ORGANIZATION_ID
    access_token = settings.LINKEDIN_ORGANIZATION_ACCESS_TOKEN

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}

    post_data = {
        "author": "urn:li:organization:"+organization_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
          "com.linkedin.ugc.ShareContent": {
           "shareMediaCategory": "NONE",
           "shareCommentary":{
            "text": text
           },
           "media": [],
           "shareCategorization": {}
          }
         },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=post_data)

    return response


