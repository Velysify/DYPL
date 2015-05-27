import unittest
import PlaylistMergerClasses


def mc_based_on_common_tastes(*matching_categories):
    #Returns a matching_category containing only the songs present in all of the playlists
    #Hopelessly ugly and ineffective, should be rewritsten
    merged_matching_category = {}
    for mc in matching_categories[0]:          
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
    merged_matching_category = {}
    playlist_number = 0

    for mc in matching_categories:
        for entry in mc.playlist_data.keys():
            if entry in merged_matching_category: #obra
                merged_matching_category[entry][0] += mc.playlist_data[entry][0]
            else:
                merged_matching_category[entry] = mc.playlist_data[entry]

        playlist_number += 1

def pl_supre_best_algorith_ever(new_playlist, *playlists):
    #For each matching category. Itterate through all the playlists and the categories.
    for index in range(0,len(playlists[0][0].matching_categories)):
            categories_to_be_merged =[]
            for playlist in playlists[0]:
                categories_to_be_merged.append(playlist.matching_categories[index])
            new_playlist.matching_categories.append(PlaylistMergerClasses.merge_matching_categories(categories_to_be_merged))
    #Return the playlist        
    return new_playlist
