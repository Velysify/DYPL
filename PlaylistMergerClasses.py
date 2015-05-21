import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import spotipy
import spotipy.util as util

spotify = spotipy.Spotify()




class Playlist:

    def __init__(self):

        token = 'BQC7BRu-M77fxGTnm9F3ptIMcU-uxKkAWT_il2MtuCiI54Q70H2RlLYYKBGlH_Fsk3JT5U7zHYnUxXtskBcmUTYwDh8ETRNkq9wU6fbFhJ5sKg_0ZswDdF0s1qmuaYgudfeFNqqjO0pP5TX_nhr032m9drZqnffv08BsL_O4AnJmgy-m7W0XD7PzYM_-nkYF2TNKgmwf7EUyZJZ7q6F2fs4eHR4FbazSKj-1yI2EFJOcd5OwbkOSiLjO6UQtj3lO3eicUh9DnFnDY5mSq-KWyVC-5XpGP0CCINFL3QnpXH2y'

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            results = sp.user_playlist('sanna_19', '2VkvjS7dNkqRiPIkgziliq', tracks)
            print results
        else:
            print "Can't get token for", username
        
        self.array_of_songs_in_playlist = [results]
        print array_of_songs_in_playlist
        matching_categories = []

    def generate_playlist(self):
        pass

class MatchingCategory:

    def __init__(self, playlist):
        self.harmony_rating = 0
        self.playlist_data = {}
    def generate_playlist(self):
        pass

    def analyze_playlist(playlist):
        pass

class MatchingCategorySong(MatchingCategory):

    def __init__(self, playlist):
        self.playlist_data = self.analyze_playlist(playlist)

        MatchingCategory.__init__(self, playlist)

    def analyze_playlist(playlist):



def merge_matching_categories(*matching_categories):
    merging_algorithm = MergingAlgorithms.mc_based_on_common_tastes(*matching_categories)

    return merging_algorithm(*matching_categories)

def merge_plalists(*playlists):
    merging_algorithm = MergingAlgorithms.pl_best(*playlists)

    return merging_algorithm(*playlists)

test = Playlist()
