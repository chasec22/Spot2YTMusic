import os
import argparse
from pprint import PrettyPrinter
import time

import tkinter as tk
import requests
from tkinter import messagebox

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
   
def get_inspirational_quote():
    response = requests.get('http://localhost:5002/get_quote')
    if response.status_code == 200:
        quote_data = response.json()
        inspirational_quote = quote_data['quote']
        print("Quote of the Day", inspirational_quote)
    else:
        print("Error", "Failed to fetch quote.")    

if __name__ == '__main__':

    while True:
        get_inspirational_quote()
        inpu = int(input("WELCOME TO SPOT2YTMUSIC!!!!\n\n!!!IMPORTANT!!! \n There are a limited number of inputs the Google API can handle a day so just remember that when creating your playlists that creating too many requests will cap you out for the day \n!!!IMPORTANT!!!\n\n Here are a few options for what we can do today!\n 1.See recent update features\n 2.Get a Quick tutorial on how the application works.\n 3.Convert songs to a playlist (Takes around 1-2 minute)\n 4.Login \n 5.Delete an Account\n 6.Rename Playlist \n 7.Exit the program\n\n Input: "))

        if inpu == 1:
            print("In the most recent update we have introduced new funtionality to the program\nWe have added the ability to create playlists from text files which is the biggest\nWe have also added a description and this update feature.\n\nPress enter to go back")
            i = input()

        elif inpu == 2:
            print("How to use Spot2YTMusic:\nStep 1: Enter test.txt file and enter in all of the songs you would like in the playlist\nStep 2: Come back here and run the program\nStep 3: When prompted again select option number 3\nStep 4: Follow the instrucions to find your playlist.\nStep 5: Keep looking around or hit option 4 to exit the program!\n\nPress enter to go back")
            i = input()

        elif inpu == 3:
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
            
            filename = "txtFiles/songs.txt"
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
           
        def get_inspirational_quote():
            response = requests.get('http://localhost:5002/get_quote')
            if response.status_code == 200:
                quote_data = response.json()
                inspirational_quote = quote_data['quote']
                print("Quote of the Day", inspirational_quote)
            else:
                print("Error", "Failed to fetch quote.")
            
        if inpu == 4:
            name = input("User name: \n")
            passw = input("Password: \n")
            
            file = open("MicroserviceA/comm.txt", "w")
            file.write(name + " " + passw)
            file.close()
            
            time.sleep(5)
            
            time.sleep(5)
            
            file = open("MicroserviceA/comm.txt", "r")
            text = file.read()
            print(text)
            file.close()
            
        if inpu == 5:
            name = input("User name: \n")
            passw = input("Password: \n")
            
            file = open("txtFiles/accountToDelete.txt", "w")
            file.write(name + " " + passw)
            file.close()
            
            input("Input when done with account deletion \n")
            
            file = open("txtFiles/accountToDelete.txt", "r")
            text = file.readline()
            print(text)
            file.close()
        
        if inpu == 6:
            newName = input("New Name: \n")
            playlistID = input("ID of playlist \n")
            with open("txtFiles/rename.txt", "w") as w:
                w.write(newName + " " + playlistID)
                
            input("Input when finished with rename.py \n")
            
            with open("txtFiles/rename.txt", "r") as r:
                text = r.readline()
                print(text)
        
        if inpu == 7:
            exit()
        
        print("\n\n\n")
