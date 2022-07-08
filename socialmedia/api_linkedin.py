import requests

from django.conf import settings


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