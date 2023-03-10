# from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

pl_id = {"default": 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF',
         "edm": 'https://open.spotify.com/playlist/37i9dQZF1DX3Kdv0IChEm9',
         "metal": 'https://open.spotify.com/playlist/37i9dQZF1EQpgT26jgbgRI',
         "rock": 'https://open.spotify.com/playlist/37i9dQZF1DWSAm0NxvFu7q'}
pl_id["mix"] = list(pl_id.values())

def get_chart(genre):
    response = dict()
    if genre == "mix":
        for playlist in pl_id["mix"]:
            response.update(sp.playlist_items(playlist,
                                 offset=0,
                                 fields='items.track.name,items.track.artists.name',
                                 additional_types=['track']))
    else:  
        response = sp.playlist_items(pl_id[genre],
                                    offset=0,
                                    fields='items.track.name,items.track.artists.name',
                                    additional_types=['track'])    
    chart = []
    for item in response["items"]:
        item = item["track"]
        chart.append({"Artist": item["name"],
                      "TrackName": item["artists"][0]["name"]})
    return chart