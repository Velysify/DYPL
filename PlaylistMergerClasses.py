import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import urllib2
import re
import time
import random
import spotipy
import spotipy.util as util

class Playlist:

    def __init__(self, token, username, playlist, playlist_max_size = 1000):
        if playlist:
            print "username:  "+str(username)
            print "playlist: "+str(playlist)
            self.token = token
            self.username = username
            self.playlist = playlist
            self.array_of_songs_in_playlist = []
            self.matching_categories = []
            self.fill_up_array_of_songs_in_playlist(self.playlist)
            self.playlist_max_size = playlist_max_size

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


    def generate_playlist(self):
        main_krover = []
        for category in self.matching_categories:
            krover = category.generate_playlist()
            main_krover.extend(krover)
        return main_krover

    def create_playlist(self, list_of_songs, name_of_playlist):
        song_list = []
        limit = None
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
            playlist = sp.user_playlist_create(self.username,name_of_playlist)
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

    def __init__(self, playlist, playlist_data_for_merged_mc, harmony_rating = 0):

        #If playlist is None and playlist_data_for_merged_mc isn't, the MatchingCategory is being initiated as as a merge between two others.
        #In that case, set playlist_data to the dictionary provided by the merging method
        if (playlist_data_for_merged_mc == None and playlist != None):
            self.playlist_data = {}
            self.playlist_data = self.analyze_playlist(playlist)
        elif (playlist_data_for_merged_mc != None and playlist== None):
            self.playlist_data = playlist_data_for_merged_mc
        else:
            raise NameError ('Vajsing!')
        
    def __str__(self):
        tjolahopp = ""

        for item_name, weight in self.playlist_data.iteritems():
            tjolahopp = tjolahopp+(item_name)+" weight: "+str(weight[0])+"\n"

        return tjolahopp
    
class MatchingCategorySong(MatchingCategory):

    def __init__(self, playlist, playlist_data_for_merged_mc, harmony_rating=0):

        MatchingCategory.__init__(self, playlist, playlist_data_for_merged_mc, harmony_rating)

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

    def __init__(self, playlist, playlist_data_for_merged_mc, harmony_rating=0):
        MatchingCategory.__init__(self, playlist, playlist_data_for_merged_mc, harmony_rating)


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

    def __init__(self, playlist, playlist_data_for_merged_mc, harmony_rating=0):
        MatchingCategory.__init__(self, playlist, playlist_data_for_merged_mc, harmony_rating)


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
    def __init__(self, playlist, playlist_data_for_merged_mc, harmony_rating=0):
        MatchingCategory.__init__(self, playlist, playlist_data_for_merged_mc, harmony_rating)
    #This method have extremly long runtime. 

    def analyze_playlist(self,playlist):
        playlist_analysis = {}
        #Make a list of strings that consists of a spotify api call and up to 50 artistids. 
        tracklist = [playlist.array_of_songs_in_playlist[x:x+50] for x in xrange(0, len(playlist.array_of_songs_in_playlist), 50)]
        for tracks in tracklist:
            href = "https://api.spotify.com/v1/artists/?ids="
            for track in tracks:
                href += track['artists'][0]['id']+","
            href = href[:-1]
            #Try until HTTP Error 429: Too many requests is raises.
            try:
                response = urllib2.urlopen(href)
                page = response.read().replace("null", "None")
                page = page[15:-2]
                pagedict = eval(page)
                for index in pagedict:
                    genres = index.get("genres")
                    if genres:
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
  

def menu(self, username, token, name_of_playlist, *playlist_uris):

    #token = 'BQCDltjecmRr1GpeXrFZJP2WyjNtYsgonM-c8TwCjmj057gSugaxTplcMDCa5H3H4z5RWhY25l2lR0r0NFmLc4TJU8dguUd3QWdgrer7yVPtpmHwfAJrWADs7gFccNsxomhDtnpGAL9u5V5tQLA7k8I5Tpzc_tLe0W1JzxeEEoXAQdX8rKLE-hceXov77ApNK-auXRh-h6X1slg'
    #username = "littaly"
    #empty_playlist = Playlist(token, username, None)
    #metal_and_top40_playlist = Playlist(token, username, '66bduhu9Juv1oeKvdYV4lQ')
    #classic_hiphop_and_rock_playlist = Playlist(token, username, '0LNfNIbJBPPNt8mCM8GQ1p')
    #schlager_and_pop_playlist = Playlist(token, username, '1GKhWgfJoDrQEnPczfNCAh')

    print "Yo, this is menu(), username is: "+str(username)
    print "Yo, this is menu(), token is: "+str(token)
    print "Yo, this is menu(), uris are: "+str(playlist_uris)
    playlists = []
    for uri in playlist_uris:
        playlists.append(Playlist(token, username, uri))


    merged_playlist = self.merge_playlists(*playlists)

    merged_playlist.create_playlist(merged_playlist.generate_playlist(name_of_playlist))

    print "here comes the merged playlist: "+str(merged_playlist.matching_categories)
    for mc in merged_playlist.matching_categories:
        print mc


