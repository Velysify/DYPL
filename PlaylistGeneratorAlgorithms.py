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

            for i in range(0, (weight_of_album * 5)):
                songs_to_return.append(songs_in_album[i])

    return songs_to_return

def funky_artist_algorithm(playlist_data):

    songs_to_return = []

    for key in self.playlist_data.keys():
        tmplist = self.playlist_data.get(key)
        weight_of_artist = tmplist[0]
        paging_object_artist = spotify.artist_albums(tmplist[1])
        albums_of_artist = paging_object['items']
        for key in albums_of_artist.keys():
            songs_to_return.append(spotify.album_tracks(key['id'])['items'])

    return songs_to_return
            
