import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import spotipy
import spotipy.util as util

spotify = spotipy.Spotify()




class Playlist:

    def __init__(self):

        token = 'BQC7BRu-M77fxGTnm9F3ptIMcU-uxKkAWT_il2MtuCiI54Q70H2RlLYYKBGlH_Fsk3JT5U7zHYnUxXtskBcmUTYwDh8ETRNkq9wU6fbFhJ5sKg_0ZswDdF0s1qmuaYgudfeFNqqjO0pP5TX_nhr032m9drZqnffv08BsL_O4AnJmgy-m7W0XD7PzYM_-nkYF2TNKgmwf7EUyZJZ7q6F2fs4eHR4FbazSKj-1yI2EFJOcd5OwbkOSiLjO6UQtj3lO3eicUh9DnFnDY5mSq-KWyVC-5XpGP0CCINFL3QnpXH2y'
        username = "sanna_19"
        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            results = sp.user_playlist(username, '2VkvjS7dNkqRiPIkgziliq')
            print results
        else:
            print "Can't get token for", username
        
        self.array_of_songs_in_playlist = [results]
        print self.array_of_songs_in_playlist
        matching_categories = []

    def generate_playlist(self):
        pass

class MatchingCategory:

    def __init__(self, array_of_songs_in_playlist):
        self.harmony_rating = 0

        #playlist_data should always be implemented as a dictionary with a string as a key and a list as value.
        #The key string represents the item of each category (genre names for a genre category, artist names for an artist category, etc.)
        #The first value of the list should always be an inte representing the "weight" of each item
        self.playlist_data = {}
    def generate_playlist(self):
        pass

    def analyze_playlist(array_of_songs_in_playlist):
        pass

class MatchingCategorySong(MatchingCategory):

    def __init__(self, playlist):
        self.playlist_data = self.analyze_playlist(playlist)

        MatchingCategory.__init__(self, playlist)

    def analyze_playlist(self, array_of_songs_in_playlist):
        #Creates the dictionary object to return
        playlist_analysis = {}

        for track in array_of_songs_in_playlist:
            #Creates an identifier for each track based on song and artist name, intended to work as a key in the dictionary
            #Using this identifier rather than the track ID means a song from an artist will always count as the same, even if it's taken from two different albums
            artist_song_identifier = str(track.name())+" - "+str(track.artists()[0].name())

            if not artist_song_identifier in self.playlist_data.keys():
                playlist_analysis[artist_song_identifier][0] = track.id()
                playlist_analysis[artist_song_identifier][1] += 1
            else:
                #is this even necessary???
                playlist_analysis[artist_song_identifier][0] = track.id()
                playlist_analysis[artist_song_identifier][1] = 1

        return playlist_analysis







def merge_matching_categories(*matching_categories):
    merging_algorithm = MergingAlgorithms.mc_based_on_common_tastes(*matching_categories)

    return merging_algorithm(*matching_categories)

def merge_plalists(*playlists):
    merging_algorithm = MergingAlgorithms.pl_best(*playlists)

    return merging_algorithm(*playlists)

test = Playlist()
