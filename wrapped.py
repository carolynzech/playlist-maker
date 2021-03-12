
# return's user's top artists

# limit: number of artists to display; max is 50
# time_range: short_term is 1 month, medium_term is 6 months, long_term is years
# uris: if True, return a list of uris; if False, return a formatted string of top artists
def top_artists(sp, limit=10, time_range='medium_term', uris=False):
    result = sp.current_user_top_artists(limit=limit, time_range=time_range)
    artists = {}
    artist_uris = []
    i = 1

    for artist in result['items']:
        artists[i] = artist['name']
        artist_uris.append(artist['uri'])
        i += 1

    if uris:
        return artist_uris
    else:
        return '\n'.join([f'\t({str(k)}) {v}' for k, v in artists.items()])


# return user's top tracks

# limit: number of tracks to display; max is 50
# time_range: short_term is 1 month, medium_term is 6 months, long_term is years
# uris: if True, return a list of uris; if False, return a formatted string of top tracks
def top_tracks(sp, limit=10, time_range='medium_term', uris=False):
    result = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    tracks = {}
    track_uris = []
    i = 1

    for track in result['items']:
        tracks[i] = ', '.join([track['name'], track['album']['artists'][0]['name'],
                               track['album']['name']])
        track_uris.append(track['uri'])
        i += 1

    if uris:
        return track_uris
    else:
        return '\n'.join([f'\t({str(k)}) {v}' for k, v in tracks.items()])
