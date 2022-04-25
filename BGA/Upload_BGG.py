import requests
import json
import getpass

"""Script adopted from:
https://www.reddit.com/r/boardgames/comments/ez86me/comment/fgmawpt/?utm_source=share&utm_medium=web2x&context=3
Upload logged plays to BGG.
"""

username = "bisforblindy"
password = getpass.getpass()

login_payload = {"credentials": {"username": username, "password": password}}
headers = {"content-type": "application/json"}

with requests.Session() as s:
    p = s.post(
        "https://boardgamegeek.com/login/api/v1",
        data=json.dumps(login_payload),
        headers=headers,
    )
    if p.status_code == 400:
        raise ValueError("Login Failed. Check username and password.")

    play_payload = {
        "playdate": "2022-04-21",
        "comments": "",
        "length": 60,
        "twitter": "false",
        "location": "BGA",
        "objectid": "205637",
        "quantity": "1",
        "action": "save",
        "date": "2022-04-20T05:00:00.000Z",
        "players": [
            {
                "username": "",
                "userid": 0,
                "repeat": "true",
                "name": "Non-BGG Friend",
                "selected": "false",
                "score": 2,
                "win": True,
                "new": True,
            },
            {
                "username": username,
                "userid": 417985,
                "name": "Brian Lindawson",
                "selected": "false",
                "score": 1,
                "win": False,
                "new": True
            },
        ],
        "objecttype": "thing",
        "ajax": 1,
    }
    r = s.post(
        "https://boardgamegeek.com/geekplay.php",
        data=json.dumps(play_payload),
        headers=headers,
    )
