import json
from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

pl_id = {"default": 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF',
         "edm": 'https://open.spotify.com/playlist/37i9dQZF1DX3Kdv0IChEm9',
         "metal": 'https://open.spotify.com/playlist/37i9dQZF1EQpgT26jgbgRI',
         "rock": 'https://open.spotify.com/playlist/37i9dQZF1DWSAm0NxvFu7q'}
offset = 0

# chart.append({
#     "Rank": entry['chartEntryData']['currentRank'],
#     "Artist": ', '.join([artist['name'] for artist in entry['trackMetadata']['artists']]),
#     "TrackName": entry['trackMetadata']['trackName']
# })


def get_chart(genre):
    response = sp.playlist_items(pl_id[genre],
                                 offset=offset,
                                 fields='items.track.name,items.track.artists.name',
                                 additional_types=['track'])
    chart = []
    for item in response["items"]:
        item = item["track"]
        chart.append({"Artist": item["name"],
                      "TrackName": item["artists"][0]["name"]})
    return chart
