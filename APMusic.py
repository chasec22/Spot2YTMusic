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

DEVELOPER_KEY = "AIzaSyDXWYRPX6dJGnrTs3aKQcTYUbziHdt-0jM"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
AUTH = "4/1AdLIrYdi4c4qRCsteySCVgqWI5d5kVxzosQLMOZuNTGMMCxH4MB9mvebuLo"
MISSING_CLIENT_SECRETS_MESSAGE = os.path.abspath(os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE))

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def add_playlist(youtube, args):
  
    body = dict(
        snippet=dict(
        title=args.title,
        description=args.description
    ),
        status=dict(
        privacyStatus='private'
    ) 
  ) 
    
    playlists_insert_response = youtube.playlists().insert(
        part='snippet,status',
        body=body
    ).execute()

    print('New playlist ID: %s' % playlists_insert_response['id'])
    return playlists_insert_response['id']

# def find_song(youtube, song):
    
def add_video_to_playlist(youtube,videoID,playlistID):
    add_video_request=youtube.playlistItems().insert(
    part="snippet",
    body={
        'snippet': {
            'playlistId': playlistID, 
            'resourceId': {
                    'kind': 'youtube#video',
                'videoId': videoID
                }
            #'position': 0
            }
    }
     ).execute()    
    

if __name__ == '__main__':

    while True:
        inpu = int(input("WELCOME TO SPOT2YTMUSIC!!!!\n\n!!!IMPORTANT!!! \n There are a limited number of inputs the Google API can handle a day so just remember that when creating your playlists that creating too many requests will cap you out for the day \n!!!IMPORTANT!!!\n\n Here are a few options for what we can do today!\n 1.See recent update features\n 2.Get a Quick tutorial on how the application works.\n 3.Convert songs to a playlist (Takes around 1-2 minute) \n 4.Exit\n\n Input: "))

        if inpu == 1:
            print("In the most recent update we have introduced new funtionality to the program\nWe have added the ability to create playlists from text files which is the biggest\nWe have also added a description and this update feature.\n\nPress enter to go back")
            i = input()

        if inpu == 2:
            print("How to use Spot2YTMusic:\nStep 1: Enter test.txt file and enter in all of the songs you would like in the playlist\nStep 2: Come back here and run the program\nStep 3: When prompted again select option number 3\nStep 4: Follow the instrucions to find your playlist.\nStep 5: Keep looking around or hit option 4 to exit the program!\n\nPress enter to go back")
            i = input()

        if inpu == 3:
            parser = argparse.ArgumentParser()
            parser.add_argument('--title',
                default='Spot2YTMusic Playlist',
                help='The title of the new playlist.')
            parser.add_argument('--description',
                default='A private playlist created with the YouTube Data API.',
                help='The description of the new playlist.')
            
            args = parser.parse_args()
            
            youtube = get_authenticated_service()
            
            playlist_id = add_playlist(youtube, args)
            
            print("Step 1. Complete! Your playlist has been created. Here is the ID. To get access to your playlist paste this code after youtube.com/ \n")
            print(playlist_id + "\n")
            
            filename = "test.txt"
            with open(filename) as file:
                songs = [song.rstrip() for song in file]
            
            print("Step 2. \n Songs: \n")
            print(songs)
                
            req = []    
            res = []
            Ids = []
            
            
            for x in range (0,len(songs)):
                req = youtube.search().list(q=songs[x],part='snippet',type='video')
                # print(type(request))
                res = req.execute()
                    
                
                Ids.append(res['items'][0]['id']['videoId'])
                
            print("Step 3. \n Song ID's: \n")
            print(Ids)
            
            for x in range (0, len(Ids)):
                add_video_to_playlist(youtube, Ids[x], playlist_id)
            
            print("\nPlaylist Created!")
            
        if inpu == 4:
            exit()
        
        print("\n\n\n")