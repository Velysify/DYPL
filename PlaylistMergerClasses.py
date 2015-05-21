import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import spotipy
import spotipy.util as util

spotify = spotipy.Spotify()




class Playlist:

    def __init__(self):

        self.array_of_songs_in_playlist = []
        token = 'BQAIwyjn2Ko3hEH7Ha-25oL1-JzdiQdyHa_7CWzJVKm2uMCpLMiwTq9Bk8YJCnGgVhY0xwDnu5xcQ6qjQbVnrN1gPOiUFvmLeCSpoQzqhKlvdUttjRjavwfSku0n9zSdNZJEEBnSfcBIKUM4jsoaeYh3X5U0sWdPfu9qEWqFc3VJG1GV7yctLiR2ySvoIGXdLeoNsGml82QyEn6tRVLn44MsDVo4b6UwpVv_ZHaEE2xyOiXT8s43yJ90u_IDeKvzTTq4gFkKp484K064sE9MTz4gi5kYMqk6d7__jU9TUICo'

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

def merge_matching_categories(*matching_categories):
    merging_algorithm = MergingAlgorithms.mc_based_on_common_tastes(*matching_categories)

    return merging_algorithm(*matching_categories)

def merge_playlists(*playlists):
    merging_algorithm = MergingAlgorithms.pl_best(*playlists)

    return merging_algorithm(*playlists)
def menu():
    playlist = Playlist()
    mc = MatchingCategorySong(playlist)
    print(mc.playlist_data)

menu()
