import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import spotipy
import spotipy.util as util

spotify = spotipy.Spotify()




class Playlist:

    def __init__(self):

        self.array_of_songs_in_playlist = []
        token = 'BQCkSiwGY8pUHjpZnp1uYSAgX-fJhIUa1U1aY_nGlC5jNTFvxw-aUwnDNkM9QtML6xIdEwLpLGMuvjsB_t0oaNLEokpUBksyjkhir0Ivg5N8VdV7QO-E3bR7Eph4tBrfr8_VNcO4_k7hqdCJSF1e5dp2xmEyzkMQipFyWSl-Gy_hf9DVcfoZFQHltXg-zkNMOBSLdniWntB_sw1amybjL0RhOy9x-FjYgNlzBVAvce3xTgEQBAYM443qJ35M3fzfPKys-BvpNEdDLx9RvTrbKcrm3cteN0D_QSvWEpY-8Fmy'

        
    
        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            playlist = sp.user_playlist('sanna_19', '6n3iKhvGFFW4j0GbwcvCBa')
            songs = playlist['tracks']
            song = songs['items']
            for i in song:
                i = i['track']
                self.array_of_songs_in_playlist.append(i)
            
        else:
            print "Can't get token for", username
        
       
        for song in self.array_of_songs_in_playlist:
            print song['name']
        
        matching_categories = []

    def generate_playlist(self):
        pass

class MatchingCategory:

    def __init__(self, playlist):
        self.playlist_data = self.analyze_playlist(playlist)
        self.harmony_rating = 0

    def generate_playlist(self):
        pass

    def analyze_playlist(playlist):
        pass

def merge_matching_categories(*matching_categories):
    merging_algorithm = MergingAlgorithms.mc_based_on_common_tastes(*matching_categories)

    return merging_algorithm(*matching_categories)

def merge_plalists(*playlists):
    merging_algorithm = MergingAlgorithms.pl_best(*playlists)

    return merging_algorithm(*playlists)

test = Playlist()
