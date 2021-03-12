import math

import main
import wrapped


# return a list of integers, where each integer is the number of tracks allocated per artist
def _tracks_per_artist(size, len_top) -> list:
    equal = math.floor(size / len_top)
    remainder = size % len_top
    per = []

    for _ in range(remainder):
        per.append(equal + 1)

    for _ in range(remainder, len_top):
        per.append(equal)

    return per


# returns the top tracks from the related artists of the user's top artists
def _recommended_songs(sp, size, num_artists, time_range) -> list:
    adding = []
    checked = []
    top_artists = wrapped.top_artists(sp, num_artists, time_range, uris=True)

    per_artist = _tracks_per_artist(size, len(top_artists))
    j = 0

    for artist_uri in top_artists:
        i = 0

        while i < per_artist[j]:
            related_uri = None

            # checks that related artist hasn't already been covered
            for related in sp.artist_related_artists(artist_uri)['artists']:
                potential = related['uri']
                if potential not in checked:
                    related_uri = potential
                    checked.append(potential)
                    break
            # if there are no related artists that haven't been covered by previous passes, break
            if related_uri is None:
                break

            try:
                top_tracks = sp.artist_top_tracks(related_uri)
                track_uri = top_tracks['tracks'][i]['uri']
            except IndexError:
                # catches when a playlist has less than i songs
                break

            if track_uri in adding:
                if per_artist[j] != 10:
                    per_artist[j] += 1
            else:
                adding.append(track_uri)

            i += 1

        j += 1

    return adding


# create a playlist for recommended songs

# size: size of the playlist. Max size is 100. Note that if related artists have too much overlap,
# the size of the playlist may not reach the inputted size. To fix this, increase num_artists.
# num_artists: the number of top artists to base the recommendations on
# time_range: short_term is 1 month, medium_term is 6 months, long_term is years
def execute(sp, username, size=10, num_artists=10, time_range='medium_term', name='Recommendations', description=None):
    main.add_tracks(sp, main.create_playlist(sp, username, name, description),
                    _recommended_songs(sp, size, num_artists, time_range))
