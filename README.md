# Playlist Maker

Playlist Maker is a Python project that allows users to have ultimate control over their playlists. Users must download the [spotipy package](https://spotipy.readthedocs.io/en/2.16.1/) and [register an app with Spotify for Developers](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app).

## Overview of Modules

### main

The foundational functions. Return existing tracks from playlists, add tracks to playlists, create playlists, or return recently played songs. Any calls to the other modules should be made in the main() function.

### playlist-sorter

Analyze audio features of tracks to see whether those tracks fit within a given playlist. If no tracks are given, the default is the user's recently played tracks. Customize the sorting further by only considering recently played songs that have been played a given number of times.

### recommender

Recommend songs for the user by getting the related artists for the user's top artists and returning their top tracks. Create a playlist of those recommended songs, customizable by size, number of top artists to consider, and more.

### wrapped

Spotify Wrapped, whenever you want. Return a given number of top artists and/or top tracks over a given period of time, formatted for easy readability.

## Example Uses

- Create a playlist of recommendations called "My Recommendations" with a playlist description "New songs to try!". Playlist is size 25, the songs are picked from 15 top artists taken from a long-term time range (about one year).

  ```python
  recommender.execute(sp, username, size=25, num_artists=15, time_range='long_term', 
                        name='My Recommendations', 
                        description=f'New songs to try!')
  ```
     
- See if your recently played tracks (that you've played at least 5 times) fit a given playlist, and if so, add them to that playlist.
  
  ```python
  playlist_sorter.execute(sp, playlist_id='insert playlist uri', threshold=5)
  ```
  
- See if a given list of potential tracks fit the given audio features of a given playlist, and if so, add them to that playlist.
  ```python
  playlist_sorter.execute(sp, playlist_id='insert playlist uri',
                            pot=['spotify:track:4U45aEWtQhrm8A5mxPaFZ7', 'spotify:track:1mea3bSkSGXuIRvnydlB5b'],
                            features=['danceability', 'energy', 'liveness'])
  ```
- Return uris of top artists/tracks over the past month.
  ```python
  wrapped.top_artists(time_range='short_term', uris=True)
  wrapped.top_tracks(time_range='short_term', uris=True)
  ```
- Print the top artists/tracks over the past month.
  ```python
  wrapped.top_artists(time_range='short_term')
  wrapped.top_tracks(time_range='short_term')
  ```
