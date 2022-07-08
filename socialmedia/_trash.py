# Here I place everything that it does not work or it is not used at the moment
import requests

from django.conf import settings



def post_text_in_linkedin_profile(text):
    # THIS FUNCTION WORKS, BUT I AM POSTING ON THE COMPANYS PAGE
    # scope: w_member_social,r_liteprofile
    profile_id = settings.LINKEDIN_PROFILE_ID
    access_token = settings.LINKEDIN_ACCESS_TOKEN

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}

    post_data = {
        "author": "urn:li:person:"+profile_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=post_data)

    return response


def post_text_in_linkedin_company(text):
    # NOT WORKING. I SEND A TICKET TO LINKEDIN
    organization_id = settings.LINKEDIN_ORGANIZATION_ID
    access_token = settings.LINKEDIN_ORGANIZATION_ACCESS_TOKEN

    url = "https://api.linkedin.com/rest/posts"

    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'LinkedIn-Version': '202206',
               'Authorization': 'Bearer ' + access_token}

    post_data = {
      "author": "urn:li:organization:"+organization_id,
      "commentary": text,
      "visibility": "PUBLIC",
      "distribution": {
        "feedDistribution": "NONE",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
      },
      "lifecycleState": "PUBLISHED",
      "isReshareDisabledByAuthor": False,
    }

    response = requests.post(url, headers=headers, json=post_data)

    return response