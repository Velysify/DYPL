def mc_based_on_common_tastes(*matching_categories):

    merged_matching_category = {}
    for mc in matching_categories:
        for entry in mc.keys():
            if entry in merged_matching_category:
                merged_matching_category[entry][0] += mc[entry][0]
            else:
                merged_matching_category[entry]

def mc_by_compromising(*matching_categories):
    pass

def pl_best(*playlists):
    pass
