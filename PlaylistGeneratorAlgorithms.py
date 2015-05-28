import spotipy

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

            for i in range(0, 1):
                songs_to_return.append(songs_in_album[i])
    """for i in range(len(songs_to_return)):
        print songs_to_return[i]['name']"""
    return songs_to_return

def funky_artist_algorithm(playlist_data):

    songs_to_return = []

    for key in playlist_data.keys():
        tmplist = playlist_data.get(key)
        weight_of_artist = tmplist[0]
        paging_object = spotify.artist_albums(tmplist[1][0]['uri'], limit = weight_of_artist)
        albums_of_artist = paging_object['items']
        for i in range(len(albums_of_artist)):
            songs_in_album = spotify.album_tracks(albums_of_artist[i]['id'])['items']
            for x in range(0, 1):
                #fix range, with weight somehow
                songs_to_return.append(songs_in_album[x])
    return songs_to_return

def funky_genre_algorithm(playlist_data):

    songs_to_return = []

    for key in playlist_data.keys():
        tmplist = playlist_data.get(key)
        weight_of_genre = tmplist[0]
        paging_object = spotify.search('genre:'+ str(tmplist[1]), limit = weight_of_genre, type = 'track')
        song_in_genre = paging_object['tracks']['items']
        for i in range(len(song_in_genre)):
            songs_to_return.append(i)

    return songs_to_return
        

    
    
            
