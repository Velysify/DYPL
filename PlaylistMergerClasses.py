import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import urllib2
import re
import time
import spotipy
import spotipy.util as util

class Playlist:

    def __init__(self, token, username, playlist):
        if playlist:
            self.token = token
            self.username = username
            self.playlist = playlist
            self.array_of_songs_in_playlist = []
            self.matching_categories = []
            self.fill_up_array_of_songs_in_playlist(self.playlist)

            create_matching_categories(self)

        #When creating a new playlist for generating playlists.     
        else:
            self.token = token
            self.username = username
            self.matching_categories = []
            self.array_of_songs_in_playlist = []

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
            print "Can't get token for" + self.username

    """def generate_matching_categories(self):
        #hardkodat, se till att det gar att konfigurera @ runtime
        print "generating matching categories"

        new_matching_category_song = MatchingCategorySong(self)
        new_matching_category_artist = MatchingCategoryArtist(self)

        self.matching_categories.append(new_matching_category_song)
        self.matching_categories.append(new_matching_category_artist)
    """


    def generate_playlist(self):
        main_krover = []

        for category in self.matching_categories:
            krover = category.generate_playlist()
            main_krover.extend(krover)
        return main_krover

    def create_playlist(self, list_of_songs):
        song_list = []
        for i in range (len(list_of_songs)):
            song_id = list_of_songs[i]['items']
            song_list.append(song_id)
        song_list = check_for_duplicates(song_list)
        tracks = [song_list[x:x+100] for x in xrange(0, len(song_list), 100)]
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            playlist = sp.user_playlist_create(self.username,"Merged Playlist!")
                
            for tracks_to_add in tracks:
                sp.user_playlist_add_tracks(self.username, playlist['id'],tracks_to_add)
        else:
            print "Can't get token for" + self.username

class MatchingCategory(object):

    def __init__(self, playlist, playlist_data_for_merged_mc):

        #If playlist is None and playlist_data_for_merged_mc isn't, the MatchingCategory is being initiated as as a merge between two others.
        #In that case, set playlist_data to the dictionary provided by the merging method
        if (playlist_data_for_merged_mc == None and playlist != None):
            self.playlist_data = {}
            self.playlist_data = self.analyze_playlist(playlist)
        elif (playlist_data_for_merged_mc != None and playlist== None):
            self.playlist_data = playlist_data_for_merged_mc
        else:
            raise NameError ('Vajsing!')
        """
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
        """

    def __str__(self):
        tjolahopp = ""

        for item_name, weight in self.playlist_data.iteritems():
            tjolahopp = tjolahopp+(item_name)+" weight: "+str(weight[0])+"\n"

        return tjolahopp

class MatchingCategorySong(MatchingCategory):

    def __init__(self, playlist, playlist_data_for_merged_mc):

        MatchingCategory.__init__(self, playlist, playlist_data_for_merged_mc)

    def analyze_playlist(self, playlist):
        #Creates the dictionary object to return
        playlist_analysis = {}

        for track in playlist.array_of_songs_in_playlist:
            #Creates an identifier for each track based on song and artist name, intended to work as a key in the dictionary
            #Using this identifier rather than the track ID means a song from an artist will always count as the same, even if it's taken from two different albums
            artist_song_identifier = ((track['name'])+" - "+ (track['artists'][0]['name'])).encode('utf-8')

            if not artist_song_identifier in playlist_analysis.keys() and artist_song_identifier not in self.playlist_data.keys():
                item = []
                item.append(1)
                item.append(track)
                playlist_analysis[artist_song_identifier] = item
            else:
                value = playlist_analysis.get(artist_song_identifier)
                new_value= value[0]+1
                value[0] = new_value

        return playlist_analysis

    def generate_playlist(self):

        self.song_list = []

        for key in self.playlist_data.keys():
            tmplist = self.playlist_data.get(key)
            self.song_list.append(tmplist[1])
        return self.song_list

class MatchingCategoryAlbum(MatchingCategory):

    def __init__(self, playlist, playlist_data_for_merged_mc):
        MatchingCategory.__init__(self, playlist, playlist_data_for_merged_mc)


    def analyze_playlist(self, playlist):
        #Creates the dictionary object to return
        playlist_analysis = {}

        for track in playlist.array_of_songs_in_playlist:
            #Creates an identifier for each track based on song and artist name, intended to work as a key in the dictionary
            #Using this identifier rather than the track ID means a song from an artist will always count as the same, even if it's taken from two different albums
            album_identifier = (track['album']['name']).encode('utf-8')
            if not album_identifier in playlist_analysis.keys() and album_identifier not in self.playlist_data.keys():
                item = []
                item.append(1)
                item.append(track['album'])
                playlist_analysis[album_identifier] = item
            else:
                value = playlist_analysis.get(album_identifier)
                new_value= value[0]+1
                value[0] = new_value
                
        return playlist_analysis

    def generate_playlist(self):

        self.song_list = PlaylistGeneratorAlgorithms.funky_album_algorithm(self.playlist_data)
        return self.song_list

class MatchingCategoryArtist(MatchingCategory):

    def __init__(self, playlist, playlist_data_for_merged_mc):
        MatchingCategory.__init__(self, playlist, playlist_data_for_merged_mc)


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
                item.append(track['artists'])
                playlist_analysis[artist_identifier] = item
            else:
                value = playlist_analysis.get(artist_identifier)
                new_value= value[0]+1
                value[0] = new_value
                
        return playlist_analysis

    def generate_playlist(self):

        self.song_list = PlaylistGeneratorAlgorithms.funky_artist_algorithm(self.playlist_data)
        return self.song_list
    
class MatchingCategoryGenre(MatchingCategory):
    def __init__(self, playlist, playlist_data_for_merged_mc):
        MatchingCategory.__init__(self, playlist, playlist_data_for_merged_mc)
    #This method have extremly long runtime. 
    def analyze_playlist(self,playlist):
        playlist_analysis = {}
        for track in playlist.array_of_songs_in_playlist:

            #Try until HTTP Error 429: Too many requests is raises.
            try:
                #For each line in the href: look for genres and clean them to make searchable strings.
                href = track['artists'][0]['href']
                for line in urllib2.urlopen(href):
                    genre = re.search('\"\s*genres\" \: .*', line)
                    if genre:
                        genre = genre.group(0).strip(",").replace(']', "").replace(' "',"").replace('" ', "").split("[")
                        if not genre[1] == " ":
                            genres = genre[1].replace('"',"").split(",")
                            for genre in genres:
                                if genre not in self.playlist_data.keys() and genre not in playlist_analysis.keys():
                                    item = []
                                    item.append(1)
                                    item.append(None)
                                    playlist_analysis[genre] = item
                                else:
                                    value = playlist_analysis.get(genre)
                                    new_value = value[0] +1
                                    value[0] = new_value
            #When Error 429 is raised read the servers reply and wait for that many seconds before continuing.                        
            except urllib2.HTTPError, err:
                if err.code == 429:
                    time.sleep(float(err.hdrs.get('Retry-After')))         
                else:
                    raise
                                
        return playlist_analysis

    def generate_playlist(self):

        self.song_list = PlaylistGeneratorAlgorithms.funky_genre_algorithm(self.playlist_data)
        return self.song_list

def create_matching_categories(playlist):
    #Finds all Subclasses of MatchingCategory, initzialise it with the entered playlist and adds it to the list.
    categories = [cls for cls in MatchingCategory.__subclasses__()]
    for category in categories:
        playlist.matching_categories.append(category(playlist, None))
                
def merge_matching_categories(*matching_categories):
    #Set the alogritm to be used
    merging_algorithm = MergingAlgorithms.mc_based_on_common_tastes
    
    return merging_algorithm(*matching_categories)
    
def merge_playlists(*playlists):
    #Create new playlist with the same username and token as the other playlists.
    new_playlist = Playlist(playlists[0].token, playlists[0].username, None)

    #Merge the playlists    
    merging_algorithm = MergingAlgorithms.pl_supre_best_algorith_ever
    return merging_algorithm(new_playlist, *playlists)

def check_for_duplicates(song_list):
   # not order preserving
   #f1 from http://www.peterbe.com/plog/uniqifiers-benchmark
   set = {}
   map(set.__setitem__, song_list, [])
   return set.keys()


def menu(self):
    #username = input("Please enter your spotify username: ")
    #print "Get a OAuth Token from https://developer.spotify.com/web-api/console/get-track/
    #token = input("Copy the access token into the program: ")
    #playlist = input("Enter the URI of first playlist to be merged: ")
    token = 'BQASOyKEiUsmlgfC4y6Eop3YTwR3BT1AH7pQpM7O86uKkvc_fuAy6fgxP8tIArxwA3wzZDvCFhvX2QDLoxpFv37PtCoynx8nXbLarQbn1xMRZxPz4i3qrwCtEOx7mTXyWSsx3t2otZrgNoCfFuvCVbBeigwqinCBlYzZl1f8jTNuPAasAKVkw_NnwR2siKeTU7-pv8NMh9AU9mY35JBI9q87dDJDtO80yT5a91-K7vtl35xUnthozN18Hv3n7tGUm5_Ov-djA-Tl6WVLmxs4CKgRQY9hXYxdvDLvZHC_Tr5n'
    username = 'sanna_19' #Token and username are testdata
    #option = input("How do you want to merge the playlists?"
    spotify = spotipy.Spotify(auth=token)
    playlists = []
    '''while playlist:
            playlists.append(Playlist.token, username, playlist)
            playlist = input("Enter the next username: ")
            playlist = input("Enter the next URI: ")
            if playlist = ""
                playlist = None
        '''
    #The playlists added below are testdata
    """p1 = Playlist(token, username, 'spotify:user:velys:playlist:2aDpdr0r4qP6YNp2227CIi')
    playlists.append(p1)
    playlists.append(Playlist(token, username, 'spotify:user:velys:playlist:1Q6ayuLj8JRZsQWagsMOgR'))
    playlists.append(Playlist(token, username, 'spotify:user:velys:playlist:3POCCOJC8A3jsGGdqtw0pY'))
    """
    playlists.append(Playlist(token, 'velys', 'spotify:user:velys:playlist:7n0np8taZhlvE0iNYjC9Gu'))
    playlists.append(Playlist(token, username, 'spotify:user:sanna_19:playlist:1hNFR8Y66XAibRx5xDnYiZ'))
    playlists.append(Playlist(token, 'velys', 'spotify:user:velys:playlist:0FK7E35FEHnvIGZZeN6wqG'))
    #playlists.append(Playlist(token, username, None))
    npl = merge_playlists(*playlists)
    npl.create_playlist(npl.generate_playlist())
    
#menu(menu)


