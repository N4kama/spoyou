#!/usr/bin/python

import json
# URL conversions.
import urllib.request
# Spotify library.
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# Youtube library
import youtube

def get_tracks_from_spotify_playlist(config, playlist_url):
    # Authenticating to Spotify
    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=config["spotify"]["client_id"],
            client_secret=config["spotify"]["client_secret"]
        )
    )

    # Get playlist from URL
    playlist = sp.user_playlist_tracks(playlist_id=playlist_url)

    trackList = []
    # For each track in the playlist.
    for i in playlist["items"]:
        # In case there's only one artist.
        if (i["track"]["artists"].__len__() == 1):
            # We add trackName - artist.
            trackList.append(i["track"]["name"] + " - " +
                             i["track"]["artists"][0]["name"])
        # In case there's more than one artist.
        else:
            nameString = ""
            # For each artist in the track.
            for index, b in enumerate(i["track"]["artists"]):
                nameString += (b["name"])
                # If it isn't the last artist.
                if (i["track"]["artists"].__len__() - 1 != index):
                    nameString += ", "
            # Adding the track to the list.
            trackList.append(i["track"]["name"] + " - " + nameString)

    return trackList

def search_track_on_youtube(config, track):
    api = youtube.API(client_id=config["youtube"]["client_id"],
              client_secret=config["youtube"]["client_secret"],
              api_key=config["youtube"]["api_key"])
    video = api.get('search', q=track, maxResults=1, type='video', order='relevance')
    return("https://www.youtube.com/watch?v="+video["items"][0]["id"]["videoId"])

if (__name__ == "__main__"):
    # Get config
    print("Reading config.json...")
    with open("config.json") as json_file:
        config = json.load(json_file)

    # Get all tracks from public playlist
    spotify_tracks = get_tracks_from_spotify_playlist(
        config,
        str(input("Insert Spotify playlist URL: ")))
    print("Tracks retrieved from spotify!")

    # Search youtube track
    songs = []
    for i in spotify_tracks:
        songs.append(search_track_on_youtube(config, i))
    print("Search finished!")

    print("URL LIST: ")
    for i in songs:
        print(i)
    
