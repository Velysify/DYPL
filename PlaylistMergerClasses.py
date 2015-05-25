import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import spotipy
import spotipy.util as util

spotify = spotipy.Spotify()




class Playlist:

    def __init__(self,playlist, option):

        self.array_of_songs_in_playlist = []
        self.matching_categories = []

        if (option == 1):
            self.fill_up_array_of_songs_in_playlist(playlist)

    def fill_up_array_of_songs_in_playlist(self, playlist):

        token = 'BQDmWYSzE-cb-rl7rMovBOJGiukBNF5uz11IQrMfltrVxuD4zHeGyXt4gQHM1jrADvuppFZQGuKk1L_L3MRcBUykBk-M9N71Fe2skzzboy_4fBqXsoyGfqWA8yLYJdh2aMFVujtnuQSFmH74w7RKYs6fMlc2mELjud0qnU0zU_CEHZAyPxFsRmowO5VatV1WE2zW0UQDS5BRGfnF5BjN95qrKqa9ZSUN_uPOUC53ud0sF26VEoEuMqLfCy2EsEeEavXMeP4I1RiDI7OfjGbHxQT12B9evb84IG51gx2jrkRD'

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            playlist = sp.user_playlist('sanna_19', playlist)
            songs = playlist['tracks']
            song = songs['items']
            for i in song:
                i = i['track']
                self.array_of_songs_in_playlist.append(i)

        else:
            print "Can't get token for", username

    def generate_matching_categories(self):
        #hårdkodat, se till att det går att konfigurera @ runtime

        self.matching_categories[0] = MatchingCategorySong(self)
    def generate_playlist(self):
        pass

class MatchingCategory:

    def __init__(self, playlist):
        self.playlist_data = self.analyze_playlist(playlist)
        self.harmony_rating = 0

        #playlist_data should always be implemented as a dictionary with a string as a key and a list as value.
        #The key string represents the item of each category (genre names for a genre category, artist names for an artist category, etc.)
        #The first value of the list should always be an inte representing the "weight" of each item
        self.playlist_data = {}

    def generate_playlist(self):
        pass

    def analyze_playlist(playlist):
        pass

class MatchingCategorySong(MatchingCategory):

    def __init__(self, playlist):
        self.playlist_data = {}
        self.playlist_data = self.analyze_playlist(playlist)

        #MatchingCategory.__init__(self, playlist)

    def analyze_playlist(self, playlist):
        #Creates the dictionary object to return
        playlist_analysis = {}

        for track in playlist.array_of_songs_in_playlist:
            #Creates an identifier for each track based on song and artist name, intended to work as a key in the dictionary
            #Using this identifier rather than the track ID means a song from an artist will always count as the same, even if it's taken from two different albums
            artist_song_identifier = str(track['name'])+" - "+ str(track['artists'][0]['name'])
            if not artist_song_identifier in playlist_analysis.keys() and artist_song_identifier not in self.playlist_data.keys():
                item = []
                item.append(1)
                item.append(track['uri'])
                playlist_analysis[artist_song_identifier] = item
            else:
                value = playlist_analysis.get(artist_song_identifier)
                new_value= value[0]+1
                value[0] = new_value
                
        return playlist_analysis

class MatchingCategoryAlbum(MatchingCategory):

    def __init__(self, playlist):
        self.playlist_data = {}
        self.playlist_data = self.analyze_playlist(playlist)

        #MatchingCategory.__init__(self, playlist)

    def analyze_playlist(self, playlist):
        #Creates the dictionary object to return
        playlist_analysis = {}

        for track in playlist.array_of_songs_in_playlist:
            #Creates an identifier for each track based on song and artist name, intended to work as a key in the dictionary
            #Using this identifier rather than the track ID means a song from an artist will always count as the same, even if it's taken from two different albums
            album_identifier = str(track['album']['name'])
            if not album_identifier in playlist_analysis.keys() and album_identifier not in self.playlist_data.keys():
                item = []
                item.append(1)
                item.append(track['album']['name'])
                playlist_analysis[album_identifier] = item
            else:
                value = playlist_analysis.get(album_identifier)
                new_value= value[0]+1
                value[0] = new_value
                
        return playlist_analysis

class MatchingCategoryArtist(MatchingCategory):

    def __init__(self, playlist):
        self.playlist_data = {}
        self.playlist_data = self.analyze_playlist(playlist)

        #MatchingCategory.__init__(self, playlist)

    def analyze_playlist(self, playlist):
        #Creates the dictionary object to return
        playlist_analysis = {}

        for track in playlist.array_of_songs_in_playlist:
            #Creates an identifier for each track based on song and artist name, intended to work as a key in the dictionary
            #Using this identifier rather than the track ID means a song from an artist will always count as the same, even if it's taken from two different albums
            artist_identifier = str(track['artists'][0]['name'])
            if not artist_identifier in playlist_analysis.keys() and artist_identifier not in self.playlist_data.keys():
                item = []
                item.append(1)
                item.append(track['artists'][0]['name'])
                playlist_analysis[artist_identifier] = item
            else:
                value = playlist_analysis.get(artist_identifier)
                new_value= value[0]+1
                value[0] = new_value
                
        return playlist_analysis

def merge_matching_categories(*matching_categories):
    merging_algorithm = MergingAlgorithms.mc_based_on_common_tastes

    return merging_algorithm(*matching_categories)
    #return MergingAlgorithms.mc_based_on_common_tastes(*matching_categories)

def merge_playlists(*playlists):
    merging_algorithm = MergingAlgorithms.pl_supre_best_algorith_ever(*playlists)

    return merging_algorithm(*playlists)

def menu(self):
    
    playlist1 = Playlist('3BVqFufvKtRenYZjG9y3to', 1)
    playlist2 = Playlist('7jqQCJtZsORrU5X2rK9px0', 1)
    playlist3 = Playlist('1hNFR8Y66XAibRx5xDnYiZ', 1)


#    merged_playlist = self.merge_playlist(playlist1, playlist2, playlist3)

    mc1 = MatchingCategoryArtist(playlist1)
    mc2 = MatchingCategoryArtist(playlist2)
    mc3 = MatchingCategoryArtist(playlist3)

    print merge_matching_categories(mc1, mc2, mc3)


    #print(mc1.playlist_data)
    #print(mc2.playlist_data)

#    print merged_playlist.matching_categories
    
    

menu(menu)
