import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import urllib2
import re
import spotipy
import spotipy.util as util

class Playlist:

    def __init__(self, token, username, playlist, option):
        self.token = token
        self.username = username
        self.playlist = playlist
        self.array_of_songs_in_playlist = []
        self.matching_categories = []


        if (option == 1):
            #change the method to one with return typ instead
            self.fill_up_array_of_songs_in_playlist(self.playlist)

        #self.generate_matching_categories()
            
        create_matching_categories(self)

    def fill_up_array_of_songs_in_playlist(self, playlist):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            sp.trace = False
            playlist = sp.user_playlist(self.username, self.playlist)
            songs = playlist['tracks']
            song = songs['items']
            for i in song:
                i = i['track']
                self.array_of_songs_in_playlist.append(i)

        else:
            print "Can't get token for", username


    """def generate_matching_categories(self):
        #hardkodat, se till att det gar att konfigurera @ runtime


        new_matching_category = MatchingCategorySong(self)
        self.matching_categories.append(new_matching_category)"""


    def generate_playlist(self):
        pass

class MatchingCategory(object):

    def __init__(self, playlist):
        self.playlist_data = {}
        self.playlist_data = analyze_playlist(playlist)
        self.harmony_rating = 0

        #playlist_data should always be implemented as a dictionary with a string as a key and a list as value.
        #The key string represents the item of each category (genre names for a genre category, artist names for an artist category, etc.)
        #The first value of the list should always be an inte representing the "weight" of each item
        

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
        playlist.matching_categories.append(self)

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
    
class MatchingCategoryGenre(MatchingCategory):
    def __init__(self, playlist):
        self.playlist_data = {}
        self.playlist_data = self.analyze_playlist(playlist)
        playlist.matching_categories.append(self)

        
    def analyze_playlist(self,playlist):
        playlist_analysis = {}
        for track in playlist.array_of_songs_in_playlist:
            href = track['artists'][0]['href']
            for line in urllib2.urlopen(href):
                genre = re.search('\"\s*genres\" \: .*', line)
                if genre:
                    genre = genre.group(0).strip(",").replace(']', "").replace(' "',"").replace('" ', "").split("[")
                    if genre[1] == " ":
                        genre[1] = None
                    if genre[1]:
                        if genre[1] not in self.playlist_data.keys() and genre[1] not in playlist_analysis.keys():
                            item = []
                            item.append(1)
                            item.append('Not Used')
                            playlist_analysis[genre[1]] = item
                        else:
                            value = playlist_analysis.get(genre[1])
                            new_value = value[0] +1
                            value[0] = new_value
                            
        return playlist_analysis

def create_matching_categories(playlist):
        categories = [cls for cls in eval('MatchingCategory').__subclasses__()]
        for category in categories:
            category(playlist)

                
def merge_matching_categories(*matching_categories):
    merging_algorithm = MergingAlgorithms.mc_based_on_common_tastes

    return merging_algorithm(*matching_categories)

def merge_playlists(*playlists):
    merging_algorithm = MergingAlgorithms.pl_supre_best_algorith_ever

    return merging_algorithm(*playlists)


#def menu(self):
    
def menu():
    #username = input("Please enter your spotify username")
    #token = input("Copy the acesstoken into the program")
    #playlist = input("Enter the URI of first playlist to be merged")
    token = 'BQA7Rlv4E7BkzeaK3AVX2zbonxjwWdkJhNJfiJdOhrK4Zx7Tbp9nNGyplYRwEWix33wOPLIfb4Dp0EGBbz4NkSoGDxpQ5AEdIdpvnvFXcnGt4l_3R_Q3LG9twBOzbrE4KIC9meUrsupu7Fu4dBtfSX2KraFSyfh2s1d5a7YKAvu2ZjHqF6CDv-p4KsW6DtDc3gs52UNDaTRR1WCyNJTtq37kAZEk70_xGaN3CxTqGwU2g7qL5YVOSXy4e6JLHdiErhhO1qUZjvWzc2kQh_40lhqor9EcWkbyYF94QLyvVlks'
    username = 'sanna_19' #Token and username are test data
    #option = input("How do you want to merge the playlists?"
    spotify = spotipy.Spotify(auth=token)
    playlists = []
    '''while playlist:
            playlists.append(Playlist.token, username, playlist)
            playlist = input("Enter the next URI")
            if playlist = ""
                playlist = None
        '''
    #The playlists added below are testdata
    playlists.append(Playlist(token, username, '3BVqFufvKtRenYZjG9y3to', 1))
    playlists.append(Playlist(token, username, '7jqQCJtZsORrU5X2rK9px0', 1))
    #playlists.append(Playlist(token, username, '1hNFR8Y66XAibRx5xDnYiZ', 1))

    merging_list = []
        
    for playlist in playlists:
        merging_list.extend(playlist.matching_categories)

    print merge_matching_categories(*merging_list)

menu()
#menu(menu)

