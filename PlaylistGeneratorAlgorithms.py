import spotipy
import random

spotify = spotipy.Spotify()

def mc_pick_at_random(matching_object):
    pass

def mc_pick_by_popularity(matching_object):
    pass

def pl_pick_best(*matching_objects):
    pass

def funky_album_algorithm(playlist_data):

    songs_to_return = []

    for key in playlist_data.keys():
            tmplist = playlist_data.get(key)
            weight_of_album = tmplist[0]
            paging_object = spotify.album_tracks(tmplist[1]['id'])
            songs_in_album = paging_object['items']

            if weight_of_album > len(songs_in_album):
                for i in range(0, len(songs_in_album)):
                    songs_to_return.append(songs_in_album[i])
            else:
                for i in range(0, weight_of_album):
                    random_index = random.randint(0, len(songs_in_album)-1)
                    songs_to_return.append(songs_in_album[random_index])

    return songs_to_return

def funky_artist_algorithm(playlist_data):

    songs_to_return = []

    for key in playlist_data.keys():
        tmplist = playlist_data.get(key)
        weight_of_artist = tmplist[0]
        top_track_catalog = spotify.artist_top_tracks(tmplist[1][0]['id'])
        top_track_catalog = top_track_catalog['tracks']
        if weight_of_artist > 10:
            songs_to_return.extend(top_track_catalog)
        elif top_track_catalog:
            for x in range(0, weight_of_artist):
                index = random.randint(0, (len(top_track_catalog)-1))
                songs_to_return.append(top_track_catalog[index])

    return songs_to_return

def funky_genre_algorithm(playlist_data):

    songs_to_return = []
    for key in playlist_data.keys():
        tmplist = playlist_data.get(key)
        weight_of_genre = tmplist[0]
        paging_object = spotify.search('genre:'+ key, limit = weight_of_genre, type = 'track')
        song_in_genre = paging_object['tracks']['items']
        for i in range(len(song_in_genre)):
            songs_to_return.append(song_in_genre[i])
    return songs_to_return
        

    
    
            
