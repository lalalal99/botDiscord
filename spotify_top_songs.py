from pprint import pprint

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

pl_id = {
    "default": 'https://open.spotify.com/playlist/37i9dQZF1DX3Kdv0IChEm9',
    "top": 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF',
    "metal": 'https://open.spotify.com/playlist/37i9dQZF1EQpgT26jgbgRI',
}
pl_id["mix"] = list(pl_id.values())


def get_songs(query):
    return sp.playlist_items(query, offset=0, fields='items.track.name,items.track.artists.name', additional_types=['track'])


def get_chart(genre):
    response = dict()
    if genre == "mix":
        response = get_songs(pl_id["mix"][0])

        for playlist in pl_id["mix"][1:]:
            songs = get_songs(playlist)
            response["items"] += (songs["items"])
    else:
        response = get_songs(pl_id[genre])

    chart = []
    for item in response["items"]:
        track = item["track"]
        chart.append({"Artist": track["artists"][0]["name"],
                      "TrackName": track["name"]})
    return chart
