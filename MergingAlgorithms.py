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
    #Create a matching category of the same type and return it.
    return matching_categories[0].__class__(None, merged_matching_category)      

def mc_by_compromising(*matching_categories):
    merged_matching_category = {}
    harmony_rating = 0


    number_of_merging_categories = len(matching_categories)
    total_playlist_weight = 0
    all_items = set()
    #creates a set of entries for each matching category, storing the keys of all items that were originally in that category
    items_in_each_playlist = [set() for x in range(number_of_merging_categories)]

    #Iterates through the matching categories, keping track (through the playlist_number variable) which matching category is the current one
    playlist_number = 0
    for mc in matching_categories:
        for entry in mc.playlist_data.keys():

            weight_of_current_entry = mc.playlist_data[entry][0]

            #keeps track of the total weight of all matching categories
            total_playlist_weight += weight_of_current_entry

            #If an entry is already added to the final, merged category, the weight is increased
            if entry in merged_matching_category: #obra
                merged_matching_category[entry][0] += weight_of_current_entry
                items_in_each_playlist[playlist_number].add(entry)
                all_items.add(entry)
            #Otherwise, it's added, in either case the entry is added to the set corresponding to the current matching category
            else:
                merged_matching_category[entry] = mc.playlist_data[entry]
                items_in_each_playlist[playlist_number].add(entry)
                all_items.add(entry)



        playlist_number += 1


    #Loops through the final merged matching category, selecting one of the original matching categories for every iteration.
    current_mc = 0

    #Calculates a threshold to be used later when determining if, and to what extent, a large enough occurence of one item in a single matching category earns it a place in the merged matching category
    #The threshold is the total amount of weights divided by the total amount of items. That is, the average amount of times each item appears in a matching category.
    if all_items:        
        threshold = total_playlist_weight/len(all_items)
        for entry in merged_matching_category.keys():

        #Checks how many of the original playlists the entry was present in
        number_of_mcs_present_in = 0
        for x in items_in_each_playlist:
            if entry in items_in_each_playlist: number_of_mcs_present_in += 1

       #Lets the entry be in the list (maintaining its total weight) if it was present in more than one of the  original matching categories
        if (number_of_mcs_present_in>1):
            harmony_rating += number_of_mcs_present_in
        #If not, but it's present in the currently selected original matching category, it is left in, but with its weight reduced to 1
        elif (entry in items_in_each_playlist[current_mc]):
            merged_matching_category[entry][0] = 1
        #Lastly, check if the entry is above the threshold for inclusion. That is, if it appears in a matching category more times than average.
        #If it does, let it stay, but with its weight divided by the average.
        elif (merged_matching_category[entry][0]>threshold):

                merged_matching_category[entry][0] = merged_matching_category[entry][0]/threshold
                if merged_matching_category[entry][0]<1: del merged_matching_category[entry]
            current_mc += 1
            if current_mc>number_of_merging_categories-1: current_mc = 0


    return matching_categories[0].__class__(None, merged_matching_category, harmony_rating)


def pl_supre_best_algorith_ever(new_playlist, *playlists):
    #For each matching category. Itterate through all the playlists and the categories.
    for index in range(0,len(playlists[0].matching_categories)):
        categories_to_be_merged =[]
        for playlist in playlists:
            categories_to_be_merged.append(playlist.matching_categories[index])
        new_playlist.matching_categories.append(PlaylistMergerClasses.merge_matching_categories(*categories_to_be_merged))
    #Return the playlist
    return new_playlist
