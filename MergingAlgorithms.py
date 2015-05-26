import unittest
import PlaylistMergerClasses


def mc_based_on_common_tastes(*matching_categories):
    #Returns a matching_category containing only the songs present in all of the playlists
    #Hopelessly ugly and ineffective, should be rewritsten
    merged_matching_category = {}
    for mc in matching_categories:
        for entry in mc.playlist_data.keys():
            if entry in merged_matching_category:
                merged_matching_category[entry][0] += mc.playlist_data[entry][0]
            else:
                merged_matching_category[entry] = mc.playlist_data[entry]

    for entry in merged_matching_category.keys():
        if merged_matching_category[entry][0]<2:
            del merged_matching_category[entry]

    return merged_matching_category


def mc_by_compromising(*matching_categories):
    pass

def pl_supre_best_algorith_ever(*playlists):
    #For testing purposes, assumes all playlists have the same number of merging categories
    merged_playlist = PlaylistMergerClasses.Playlist("lol", 2)

    unmerged_matching_categories_for_new_playlist = []
    counter = 0
    for playlist in playlists:
        unmerged_matching_categories_for_new_playlist.append([])
        for x in playlist.matching_categories:
            unmerged_matching_categories_for_new_playlist[counter].append(x)

    merged_matching_categories_for_new_playlist = []

    counter = 0
    for entry in unmerged_matching_categories_for_new_playlist:
        merged_matching_categories_for_new_playlist.append( PlaylistMergerClasses.merge_matching_categories(*entry))

    merged_playlist.matching_categories = merged_matching_categories_for_new_playlist

    return merged_playlist
