from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from flask import jsonify

load_dotenv()

test_playlist = "https://open.spotify.com/playlist/2Uqk27clDOfOoRArDXmpxC?si=79339a63358c406a"

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
     auth_string = client_id + ":" + client_secret
     auth_bytes = auth_string.encode("utf-8")
     auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
     
     url = "https://accounts.spotify.com/api/token"
     headers = {
          "Authorization": "Basic " + auth_base64,
          "Content-Type": "application/x-www-form-urlencoded"
     }
     data = {"grant_type": "client_credentials"}
     result = post(url, headers=headers, data=data)
     json_result = json.loads(result.content)
     token = json_result["access_token"]
     return token

def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

def get_playlist_tracks(token, spotID):
     playlist_id = spotID
     headers = get_auth_headers(token)
     url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

     query = "?fields=items(track(name))"
     query_url = url + query
     result = get(query_url, headers=headers)
     json_result = json.loads(result.content)
     return json_result["tracks"]

token = get_token()
res = get_playlist_tracks(token, "4CEfz1h167j8BqsVve7DbR?si=4bb3be2481a74f34")
file = open("txtFiles/songs.txt", "w")
for x in range(0, res["total"]):
     file.write(res["items"][x]["track"]["name"] + " - " + str(res["items"][x]["track"]["artists"][0]["name"]) + "\n")
