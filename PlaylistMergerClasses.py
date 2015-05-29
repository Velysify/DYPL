import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import urllib2
import re
import time
import random
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

        self.matching_categories.append(new_matcshing_category_song)
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
        limit = 1
        for i in range(len(list_of_songs)):
            song_id = list_of_songs[i]['id']
            song_list.append(song_id)
        #Remove identical songs from the playlist
        song_list = check_for_duplicates(song_list)
        random.shuffle(song_list)
        #Split into parts with a list of 100 ids in each index. (user_playlist_add_tracks has a limit of 100 tracks per call)
        tracks = [song_list[x:x+100] for x in xrange(0, len(song_list), 100)]
        #If there is still a token create and fill the new playlist with tracks.
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            playlist = sp.user_playlist_create(self.username,"Merged Playlist!")
            if not limit:
                for tracks_to_add in tracks:
                    sp.user_playlist_add_tracks(self.username, playlist['id'],tracks_to_add)
            else:
                for x in xrange(0, limit):
                    sp.user_playlist_add_tracks(self.username, playlist['id'],tracks[x])
        #Else print a statement
        else:
            print "Can't get token for" + self.username

class MatchingCategory(object):

    def __init__(self, playlist, playlist_data_for_merged_mc, harmony_rating=0):

        #If playlist is None and playlist_data_for_merged_mc isn't, the MatchingCategory is being initiated as as a merge between two others.
        #In that case, set playlist_data to the dictionary provided by the merging method
        if (playlist_data_for_merged_mc == None and playlist != None):
            self.playlist_data = {}
            self.playlist_data = self.analyze_playlist(playlist)
            self.harmony_rating = harmony_rating
        elif (playlist_data_for_merged_mc != None and playlist== None):
            self.playlist_data = playlist_data_for_merged_mc
            self.harmony_rating = harmony_rating

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
            album_identifier = track['album']['name']
            album_identifier = album_identifier.encode('utf-8')
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
            artist_identifier = track['artists'][0]['name']
            artist_identifier = artist_identifier.encode('utf-8')
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
        tracklist = [playlist.array_of_songs_in_playlist[x:x+50] for x in xrange(0, len(playlist.array_of_songs_in_playlist), 50)]
        for tracks in tracklist:
            href = "https://api.spotify.com/v1/artists/?ids="
            for track in tracks:
                href += track['artists'][0]['id']+","
            href = href[:-1]
            #Try until HTTP Error 429: Too many requests is raises.
            try:
                #For each line in the href: look for genres and clean them to make searchable strings.
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
                    print("Retry!")
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
    merging_algorithm = MergingAlgorithms.mc_by_compromising
    
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
    token = 'BQDdCsYUvwE14-ayV3b0xQhOSqSIZEW-tHK8xWhY_GPv7FozGaO9KiehDw6bPz6Knl28fyW42UMmdpw0BJahPW823GV2g91L9hzG013yA_C2qkM3_TaC_Itd2ZD7DyrpiIX0HLxih5cfK2cehG9pFOhtYwE4bwnrSHVh6-iHUP9Jqj3EHjeqivDRR3uErQ6ir59jDXxvLLE5xA-ihTCp-_9IzxotWW-utJHIxIsj-_G4haBcwytem-3xFctD-bc0DtXZtMChU2fBkxUzVeLlOVqreiv8B-kghyRkaT-pefeN'
    username = 'velys' #Token and username are testdata
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
    playlists.append(Playlist(token, 'kygoofficial', 'spotify:user:kygoofficial:playlist:7wYC2trtKwO73LskQGJLas'))
    playlists.append(Playlist(token, 'sanna_19', 'spotify:user:sanna_19:playlist:1cC4fqs5YtUlmYd6t4T4Ap'))
    playlists.append(Playlist(token, username, 'spotify:user:velys:playlist:0FK7E35FEHnvIGZZeN6wqG'))
    #playlists.append(Playlist(token, username, None)
    
    token = 'BQCDltjecmRr1GpeXrFZJP2WyjNtYsgonM-c8TwCjmj057gSugaxTplcMDCa5H3H4z5RWhY25l2lR0r0NFmLc4TJU8dguUd3QWdgrer7yVPtpmHwfAJrWADs7gFccNsxomhDtnpGAL9u5V5tQLA7k8I5Tpzc_tLe0W1JzxeEEoXAQdX8rKLE-hceXov77ApNK-auXRh-h6X1slg'
    username = "littaly"
    empty_playlist = Playlist(token, username, None)
    metal_and_top40_playlist = Playlist(token, username, '66bduhu9Juv1oeKvdYV4lQ')
    classic_hiphop_and_rock_playlist = Playlist(token, username, '0LNfNIbJBPPNt8mCM8GQ1p')
    schlager_and_pop_playlist = Playlist(token, username, '1GKhWgfJoDrQEnPczfNCAh')

    merged_playlist = self.merge_playlists(metal_and_top40_playlist, classic_hiphop_and_rock_playlist, schlager_and_pop_playlist)


    mc1 = MatchingCategorySong(metal_and_top40_playlist, None)
    mc2 = MatchingCategorySong(classic_hiphop_and_rock_playlist, None)
    mc3 = MatchingCategorySong(schlager_and_pop_playlist, None)

    #print(mc1.playlist_data)
    #print(mc2.playlist_data)


    print "here comes the merged playlist: "+str(merged_playlist.matching_categories)
    for mc in merged_playlist.matching_categories:
        print mc






#menu()



