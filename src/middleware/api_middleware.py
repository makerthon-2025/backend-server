import requests

def verify_token(req, token):
    if token and token.startswith("Bearer "):
        token = token[len("Bearer "):]
        
        res = requests.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={token}")

        req.state.email = res.json()['email']
    else:
        raise Exception("No token found")