import google 
import os
import argparse
from pprint import PrettyPrinter
import httplib2

import google.oauth2.credentials
import google_auth_oauthlib.flow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.file import Storage

DEVELOPER_KEY = os.getenv("DEVELOPER_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
AUTH = os.getenv("AUTH")
MISSING_CLIENT_SECRETS_MESSAGE = os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))
TEST_ID = ""

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def renamePlaylist(youtube, name, playlistID):
    request_body = {
                "id": playlistID,
                "snippet": {
                    "title": name,
                    "description": "New playlist description"
                },
                "status": {
                    "privacyStatus": "private"
                }
                }   
    renamePlaylistRequest = youtube.playlists().update(
        part='snippet,status',
        body=request_body
    ).execute()
    
    with open("txtFiles/rename.txt", "w") as w:
        w.write("Successfully Renamed!")
    
    
if __name__ == "__main__":

    youtube = get_authenticated_service()

    file = open("txtFiles/rename.txt", "r")
    nameAndID = file.read()
    file.close()
    
    temp = nameAndID.split(" ")
    
    renamePlaylist(youtube, temp[0], temp[1])
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--title',
        default=name,
        help='The title of the new playlist.')
    
    args = parser.parse_args()
    
    body = dict(
        snippet=dict(
            title=args.title
        )
    )'''
    
    
    