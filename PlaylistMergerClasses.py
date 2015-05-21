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
