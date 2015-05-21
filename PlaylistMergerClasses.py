import PlaylistGeneratorAlgorithms
import MergingAlgorithms
import spotipy
import spotipy.util as util

class Playlist:
    def __init__(self):
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
