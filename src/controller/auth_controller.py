from fastapi import Request
from fastapi.responses import RedirectResponse

def login_controller():
    return RedirectResponse(__get_google_login_url())


def google_callback_controller(req: Request):
    code = req.query_params.get('code')
    state = req.query_params.get('state')

    return RedirectResponse(__verify_codde_and_get_google_fe_redirect_url(code))



# ===============================
# PRIVATE FUNCTION
import os
import requests

def __get_google_login_url():
    host_url = f"{os.getenv('HOST')}:{os.getenv('SERVER_PORT')}"
    url = f"https://accounts.google.com/o/oauth2/auth?client_id={os.getenv('GOOGLE_CLIENT_ID')}&redirect_uri={host_url}{os.getenv('GOOGLE_REDIRECT_URI')}&response_type={os.getenv('GOOGLE_RESPONSE_TYPE')}&scope={os.getenv('GOOGLE_SCOPE')}&access_type={os.getenv('GOOGLE_ACCESS_TYPE')}&prompt={os.getenv('GOOGLE_PROMPT')}"
    return url

def __verify_codde_and_get_google_fe_redirect_url(code):
    REDIRECT_URI = f"{os.getenv('HOST')}:{os.getenv('SERVER_PORT')}{os.getenv('GOOGLE_REDIRECT_URI')}"
    CLIENT_SECRET=os.getenv('GOOGLE_CLIENT_SECRET')
    CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
    TOKEN_URL="https://oauth2.googleapis.com/token"

    payload = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    response = requests.post(TOKEN_URL, data=payload)

    token_data = response.json()

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token", None)

    return f"{os.getenv('GOOGLE_REDIRECT_URL_FOR_FE')}?access_token={access_token}&refresh_token={refresh_token}"