# Presentation

SpoYou is a python script listing every song on a spotify (public) playlist
onto youtube. The result is a simple URL list of every song.

# Requirements

- Python 3
- Pip (for python3)

```sh
pip install spotipy --upgrade
pip install youtube-python
```

You will **need to** edit the `config.json` file :
- Spotify : Go to https://developer.spotify.com/dashboard/applications 
and create an app. Copy paste the client id and secret generated.
- Youtube : Go to https://console.developers.google.com/
and go to `credentials`. Create one API key and one OAuth2 ID (choose Desktop app).
Copy both the API key and the ClientId/Secret from OAuth.

# Installation & Usage

```sh
git clone https://github.com/N4kama/spoyou
cd spoyou
./spoyou.py

./spoyou.py [-h | --help] [-p playlist_url | --playlistUrl playlist_url] [-o file | --output file]
```