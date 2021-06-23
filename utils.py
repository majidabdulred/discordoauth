import time
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv()

REDIRECT_URI = 'http://abdulmajidred.pythonanywhere.com/oauth/discord'

CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")


def exchange_code(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify guilds'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url='https://discord.com/api/oauth2/token',
                        data=data,
                        headers=headers)
    res.raise_for_status()
    return res.json()


def refresh_token(token):
    print("Refresh token")
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(url='https://discord.com/api/oauth2/token', data=data, headers=headers)
    r.raise_for_status()
    return r.json()


def get_me(token):
    if "exp" in token.keys() and token["exp"] < int(time.time()):
        token = update_token(token)
        print("Token Updates")
    res = requests.get("https://discord.com/api/v8/users/@me",
                       headers={"Authorization": f"Bearer {token['access_token']}"})
    res.raise_for_status()
    return res.json()


def get_guilds(token):
    res = requests.get("https://discord.com/api/v8/users/@me/guilds",
                       headers={"Authorization": f"Bearer {token['access_token']}"})
    res.raise_for_status()

    return res.json()


def update_token(token):
    data = Users.query.filter_by(access_token=token["access_token"]).first()
    res = refresh_token(token["refresh_token"])
    data.access_token = res["access_token"]
    data.refresh_token = res["refresh_token"]
    data.exp = int(time.time()) + 50000
    db.session.commit()
    return res
