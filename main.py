import spotipy
from spotipy.oauth2 import SpotifyOAuth

import datetime
import recommender
import playlist_sorter
import wrapped


# return URIs of recently played tracks
def recently_played(sp, full=False) -> list:
    if full:
        return [item['track'] for item in sp.current_user_recently_played()['items']]
    else:
        return [item['track']['uri'] for item in sp.current_user_recently_played()['items']]


# return URIs of tracks already in a given playlist
def existing_tracks(sp, playlist_id, full=False) -> list:
    playlist_items = sp.playlist_items(playlist_id)

    if playlist_items is None:
        return []
    elif full:
        return [item['track'] for item in playlist_items['items']]
    else:
        return [item['track']['uri'] for item in playlist_items['items']]


# add songs to a given playlist
def add_tracks(sp, playlist_id, song_ids):
    adding = []
    existing = existing_tracks(sp, playlist_id)

    for song_uri in song_ids:
        if song_uri not in existing and song_uri not in adding:
            adding.append(song_uri)

    if adding:
        sp.playlist_add_items(playlist_id, items=adding)


# create a playlist, return playlist id
def create_playlist(sp, username, name='Recommendations', description=None) -> str:
    if description is None:
        description = f'Recommended songs for {datetime.date.today().strftime("%m/%d/%y")}'

    sp.user_playlist_create(username, name, collaborative=False, description=description)
    return sp.user_playlists(username, limit=1)['items'][0]['uri']


def main():

    username = 'XXX'
    client_id = 'XXX'
    client_secret = 'XXX'
    redirect_uri = 'http://localhost:8888/callback/'
    scope = 'user-top-read user-read-recently-played playlist-modify-public playlist-modify-private'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                                   redirect_uri=redirect_uri, scope=scope))

    # make calls to other modules here!


if __name__ == '__main__':
    main()
