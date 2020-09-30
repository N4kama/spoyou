#!/usr/bin/python

import sys
import getopt
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
    video = api.get('search', q=track, maxResults=1,
                    type='video', order='relevance')
    return("https://www.youtube.com/watch?v="+video["items"][0]["id"]["videoId"])


"""
    Main function
"""
if (__name__ == "__main__"):
    playlist_url = None
    outputfile = None

    # Checking arguments
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hp:o:", ["help", "playlistUrl=", "output="])
    except getopt.GetoptError:
        print(
            "./spoyou.py [-h | --help] [-p playlist_url | --playlistUrl playlist_url] [-o file | --output file]")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print(
                "./spoyou.py [-h | --help] [-p playlist_url | --playlistUrl playlist_url] [-o file | --output file]")
            sys.exit()
        elif opt in ("-p", "--playlistUrl"):
            playlist_url = arg
        elif opt in ("-o", "--output"):
            outputfile = arg

    # Get config
    print("Reading config.json...")
    with open("config.json") as json_file:
        config = json.load(json_file)

    # Get all tracks from public playlist
    if not playlist_url:
        playlist_url = str(input("Insert Spotify playlist URL: "))
    spotify_tracks = get_tracks_from_spotify_playlist(config, playlist_url)
    print("{} tracks retrieved from spotify!".format(len(spotify_tracks)))

    # Search youtube track
    songs = []
    for i in spotify_tracks:
        songs.append(search_track_on_youtube(config, i))
    print("Search finished!")

    print("URL LIST: ")
    for i in songs:
        print(i)

    if outputfile:
        print("Writting URLs to file : {}".format(outputfile))
        with open(outputfile, "w+") as url_file:
            for s in songs:
                url_file.write(s)