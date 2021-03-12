import main


# return songs played the threshold number of times or more
def _parse(sp, exi, threshold) -> list:
    recent = sp.current_user_recently_played()['items']
    over_threshold = []
    count = {}

    for track in recent:
        track_uri = track['track']['uri']
        if track_uri not in exi:
            if threshold == 0:
                over_threshold.append(track_uri)
            else:
                if track_uri not in count.keys():
                    count[track_uri] = 1
                elif count[track_uri] == threshold - 1 and track_uri not in over_threshold:
                    over_threshold.append(track_uri)
                else:
                    count[track_uri] += 1

    return over_threshold


# return tracks whose features are all within the range of features for the songs already in the playlist
def _fits(features, exi_features, pot) -> list:
    adding = []
    min_max = {}

    # initialize
    for feature in features:
        min_max[feature] = [exi_features[0][feature], exi_features[0][feature]]

    # create dictionary of feature -> [min, max] values in playlist
    for track in exi_features:
        if track is not None:
            for feature in features:
                if track[feature] < min_max[feature][0]:
                    min_max[feature][0] = track[feature]
                elif track[feature] > min_max[feature][1]:
                    min_max[feature][1] = track[feature]

    # count how many tracks in pot are within the min, max range established above
    for track in pot:
        count = 0
        for feature in features:
            if min_max[feature][0] <= track[feature] <= min_max[feature][1]:
                count += 1

        if count == len(features):
            adding.append(track['uri'])

    return adding


# add tracks to a given playlist if they fit the given features of that playlist

# playlist_id: the playlist uri (string)
# features: list of audio features to consider; full options are "danceability", "energy", "key", "loudness", "mode",
# "speechiness", "acousticness", "instrumentalness", "liveness", "valence", and "tempo"
# pot: list of potential tracks to add to the playlist; default is recently played tracks
# threshold: number of times recently played track has to be played to be considered; this field is only available
# when the potential tracks are the recently played tracks
def execute(sp, playlist_id, features=None, pot=None, threshold=0):
    exi = main.existing_tracks(sp, playlist_id)
    exi_features = sp.audio_features(exi)

    if pot is None:
        pot_features = sp.audio_features(_parse(sp, exi, threshold))
    else:
        pot_features = sp.audio_features(pot)

    if features is None:
        features = ['danceability', 'energy', 'loudness', 'mode', 'acousticness', 'instrumentalness', 'valence',
                    'tempo']

    main.add_tracks(sp, playlist_id, _fits(features, exi_features, pot_features))
