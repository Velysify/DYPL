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
            self.fill_up_array_of_songs_in_playlist(token, playlist)
            self.generate_matching_categories()
        print("size of array_of_songs is: "+str(len(self.array_of_songs_in_playlist)))
    def fill_up_array_of_songs_in_playlist(self, token, playlist):


        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            playlist = sp.user_playlist(self.username, self.playlist)
            songs = playlist['tracks']
            song = songs['items']
            for i in song:
                i = i['track']
                self.array_of_songs_in_playlist.append(i)

        else:
            print "Can't get token for",

    def generate_matching_categories(self):
        #hardkodat, se till att det gar att konfigurera @ runtime
        print "generating matching categories"

        new_matching_category_song = MatchingCategorySong(self)
        new_matching_category_artist = MatchingCategoryArtist(self)

        self.matching_categories.append(new_matching_category_song)
        self.matching_categories.append(new_matching_category_artist)


    def generate_playlist(self):
        pass

class MatchingCategory:

    def __init__(self, playlist):
        self.playlist_data = {}
        self.playlist_data = self.analyze_playlist(playlist)
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

                
def merge_matching_categories(*matching_categories):
    merging_algorithm = MergingAlgorithms.mc_based_on_common_tastes

    return merging_algorithm(*matching_categories)

def merge_playlists(*playlists):
    merging_algorithm = MergingAlgorithms.pl_supre_best_algorith_ever

    return merging_algorithm(*playlists)


def menu(self):


    token = 'BQCS8QZ1tVR1Kk-sFt6UmHHDq-q2HJ6YMG1NKzzLO5G20wkES1PG-IgREEcrv4J4cTqTLyy6KognA0Qd4BUAMgAQORR7v5cFh6hm8qcJja79j6y1sOvUBC7ZNtquKU1mJz9ZMUMJ3LhBvpotVgpdmCxyGOD2t5Xl4VLjKFLnUIGa-nSFOWSVPOzI8P8foq5EJO12kSsxBjQaDApXhdSdL8quzMSIY9x4Q8ujTXH9qVV1vysiSNYCfrmiBSoQBLPpeXh7yUClJhD1OBEvEFcYjF2hm1PH93reheDx0OYpqlWa'
    username = "sanna_19"
    playlist1 = Playlist(token, username, "3BVqFufvKtRenYZjG9y3to", 1)
    playlist2 = Playlist(token, username, '7jqQCJtZsORrU5X2rK9px0', 1)
    playlist3 = Playlist(token, username, '1hNFR8Y66XAibRx5xDnYiZ', 1)

    merged_playlist = self.merge_playlists(playlist1, playlist2, playlist3)


    mc1 = MatchingCategorySong(playlist1)
    mc2 = MatchingCategorySong(playlist2)
    mc3 = MatchingCategorySong(playlist3)


    #print(mc1.playlist_data)
    #print(mc2.playlist_data)


    print "here comes the merged playlist: "+str(merged_playlist.matching_categories)



#menu(menu)

