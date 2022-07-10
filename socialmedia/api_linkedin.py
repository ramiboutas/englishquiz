import requests

from django.conf import settings



class AbractLinkedinCompanyPageAPI:
    def __init__(self) -> None:
        access_token = settings.LINKEDIN_ORGANIZATION_ACCESS_TOKEN
        self.headers = {'Content-Type': 'application/json',
                        'X-Restli-Protocol-Version': '2.0.0',
                        'Authorization': 'Bearer ' + access_token}
        


class LinkedinCompanyPagePostAPI(AbractLinkedinCompanyPageAPI):
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
        return response



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



{'author': 'urn:li:organization:86603021',
'lifecycleState': 'PUBLISHED',
'specificContent': {
    'com.linkedin.ugc.ShareContent': {
        'shareMediaCategory': 'NONE',
        'shareCommentary': {
            'text': 'Here comes some text... Lets see if it works'
            },
'media': [],
'shareCategorization': {}}},
'visibility':{
    'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
    }
}