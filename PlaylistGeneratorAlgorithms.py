def mc_pick_at_random(matching_object):
    pass

def mc_pick_by_popularity(matching_object):
    pass

def pl_pick_best(*matching_objects):
    pass

def funky_album_algorithm(playlist_data):

    songs_to_return = []

    for key in self.playlist_data.keys():
            tmplist = self.playlist_data.get(key)
            weight_of_album = tmplist[0]
            paging_object = spotify.album_tracks(tmplist[1])
            songs_in_album = paging_object['items']

            for i in range(0, (weight_of_album)):
                songs_to_return.append(songs_in_album[i])

    return songs_to_return

def funky_artist_algorithm(playlist_data):

    songs_to_return = []

    for key in self.playlist_data.keys():
        tmplist = self.playlist_data.get(key)
        weight_of_artist = tmplist[0]
        paging_object_artist = spotify.artist_albums(tmplist[1], limit = weight_of_artist)
        albums_of_artist = paging_object['items']
        for key in albums_of_artist.keys():
            songs_in_album = spotify.album_tracks(key['id'])['items']
            for i in range(0, weight_of_artist):
                songs_to_return.append(songs_in_album[i])

    return songs_to_return

def funky_genre_algorithm(playlist_data):

    songs_to_return = []

    for key in self.playlist_data.keys():
        tmplist = self.playlist_data.get(key)
        weight_of_genre = tmplist[0]
        paging_object = spotify.search('genre:'+tmplist[1], limit = weight_of_genre, type = 'track')
        song_in_genre = paging_object['tracks']['items']
        for key in song_in_genre.keys():
            songs_to_return.append(key)

    return songs_to_return
        

    
    
            
