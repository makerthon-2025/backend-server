import requests

def get_info_controller(token):
    res = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {token}"})

    return res.json()