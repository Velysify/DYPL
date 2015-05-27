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
    merged_matching_category = {}

    number_of_merging_categories = len(matching_categories)
    #calculate the total amount of songs in all of the playlists
    total_playlist_size = 0
    for mc in matching_categories:
        total_playlist_size += len(mc.playlist_data)

    #creates a set of entries for each matching category
    items_in_each_playlist = [[] for x in range(number_of_merging_categories)]

    #Iterates through the matching categories, keping track (through the playlist_number variable) which matching category is the current one
    playlist_number = 0
    for mc in matching_categories:
        for entry in mc.playlist_data.keys():
            #If an entry is already added to the final, merged category, the weight is increased
            if entry in merged_matching_category: #obra
                merged_matching_category[entry][0] += mc.playlist_data[entry][0]
                items_in_each_playlist[playlist_number].append(entry)
            #Otherwise, it's added, in either case the entry is added to the set corresponding to the current matching category
            else:
                merged_matching_category[entry] = mc.playlist_data[entry]
                items_in_each_playlist[playlist_number].append(entry)


        playlist_number += 1
    #Loops through the final merged matching category, selecting one of the original matching categories for every iteration.
    #Deletes the entry if the weight is not above 2, or the entry was not present in the original matching category that is currently selected
    current_mc = 0
    for entry in merged_matching_category.keys():

        boolean = entry in items_in_each_playlist[current_mc]
        if merged_matching_category[entry][0]>=2 or (merged_matching_category[entry] in items_in_each_playlist[current_mc]):
            pass
        else:
            del merged_matching_category[entry]
        current_mc += 1
        if current_mc>number_of_merging_categories-1: current_mc = 0

    return merged_matching_category



def pl_supre_best_algorith_ever(empty_playlist, *playlists):
    #For testing purposes, assumes all playlists have the same number of merging categories
    merged_playlist = empty_playlist


    unmerged_matching_categories_for_new_playlist = [[] for i in range(len(playlists[0].matching_categories))]
    counter = 0
    #for each of the playlists passed as argument...
    for matching_category in playlists[0].matching_categories:
        for list in playlists:
            unmerged_matching_categories_for_new_playlist[counter].append(list.matching_categories[counter])
        counter += 1 #tror jag...

    merged_matching_categories_for_new_playlist = []

    counter = 0
    for entry in unmerged_matching_categories_for_new_playlist:
        merged_matching_categories_for_new_playlist.append(PlaylistMergerClasses.merge_matching_categories(*entry))
        counter += 1

    merged_playlist.matching_categories = merged_matching_categories_for_new_playlist

    return merged_playlist
