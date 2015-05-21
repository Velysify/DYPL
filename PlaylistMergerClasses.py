import PlaylistGeneratorAlgorithms
import MergingAlgorithms

class Playlist:
    def __init__(self):
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