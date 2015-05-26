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
            #change the method to one with return typ instead
            self.fill_up_array_of_songs_in_playlist(playlist)

        self.generate_matching_categories()

    def fill_up_array_of_songs_in_playlist(self, playlist):
        token = 'BQDTQhtVPfIdE1sZMV-0Yg1_CHKa73kh-90O_c4P2TIuKaubLSdBT8iFs8x31UdN8dwZ3ghQ-0jP7AQIYWa2fPkxhT2lSBnnCM_Fk2f58ExraiNUQWlV5tNQdLqRHXWcFatoD2IS4MAEXdpFmU9ZTDObxwA4v9Maub_xBytK7IpYM__IyaUUJxmZkGn_5vpvnRGQcOY11-C_2df2f__58AghSHy-AfMRanersd1mgkBdDW4kRMKcHoTcntXCsQsrXwy4r6TTTmdmcTdayafkCj5B6kdFNlRH6-HFEzedJBfX'


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
            print "Can't get token for",

    def generate_matching_categories(self):
        #hardkodat, se till att det gar att konfigurera @ runtime

        new_matching_category = MatchingCategorySong(self)


        self.matching_categories.append(new_matching_category)

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

    #Returns an array of Spotify songs, later used by the Playlist-object to create a Spotify playlist
    def generate_playlist(self):
        pass
    #Analyzes the array of songs (passed as the parameter 'playlist'), returns a dictionary with keys and weights to be stored in the playlist_data variable
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

def merge_playlists(*playlists):
    merging_algorithm = MergingAlgorithms.pl_supre_best_algorith_ever

    return merging_algorithm(*playlists)

def menu(self):
    
    playlist1 = Playlist('3BVqFufvKtRenYZjG9y3to', 1)
    playlist2 = Playlist('7jqQCJtZsORrU5X2rK9px0', 1)
    playlist3 = Playlist('1hNFR8Y66XAibRx5xDnYiZ', 1)


    merged_playlist = self.merge_playlists(playlist1, playlist2, playlist3)


    mc1 = MatchingCategoryArtist(playlist1)
    mc2 = MatchingCategoryArtist(playlist2)
    mc3 = MatchingCategoryArtist(playlist3)


    #print merge_matching_categories(mc1, mc2, mc3)


    #print(mc1.playlist_data)
    #print(mc2.playlist_data)


    print "here comes the merged playlist: "+str(merged_playlist.matching_categories)
    
    

#menu(menu)

