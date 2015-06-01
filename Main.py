import PlaylistMergerClasses
import MergingAlgorithms
instance = PlaylistMergerClasses


exit = False

#test data ---------------------------------------------------------------
test_token = 'BQAw8gHO_ZkqX76w_7rCza2w42EyqEjpnZ3wJ9cOczStfs5kOjJW0TYQ8zY7oL906Nw_LPVS5OSsx4N7_rQqo5xGpZczEmKJ60qonNvU4zfBgdPwXVt6yQWdC-ttxAJGR8Sm2Q_LU5y6DABdhiCPAqgoO2v0VwnZM7MyKHMK6BIbVOtZW_W0mqSTm6UuY2Q1IACEpigGQa-14CFd1fCzbGlZ9dM315WEXHLs5pF_qP9b1a3X'
test_username = "velys"
test_algo = "Based_on_common_tastes"
test_playlist = "Simple_merger"
metal_and_top40_playlist = PlaylistMergerClasses.Playlist(test_token, test_username, '7n0np8taZhlvE0iNYjC9Gu')
classic_hiphop_and_rock_playlist = PlaylistMergerClasses.Playlist(test_token, test_username, '3jeoIpQpRdDrPskLdcRVW0')
schlager_and_pop_playlist = PlaylistMergerClasses.Playlist(test_token, test_username, '0FK7E35FEHnvIGZZeN6wqG')
#test data ----------------------------------------------------------------



while (not exit):
    print "Welcome to the Spotify Playlist Merger"

    username = raw_input("Please enter your account username: ")
    token = raw_input("Please enter the access token for your account: ")

    done = False
    counter = 1
    playlists = []
    inpp = raw_input("Now enter the URIs of the playlists you wish to merge, type \'done\' when you're done, \'test\' to run with default testdata or anything else to proceed: ")

    if (inpp.lower() == "done"):
        exit = True
    elif (inpp.lower() == "test"):
        instance.menu(instance, test_username, test_token, test_algo, test_playlist, metal_and_top40_playlist, classic_hiphop_and_rock_playlist, schlager_and_pop_playlist)
    else:

        while (not done):
            inpu = raw_input("Please enter the username for the next playlist: ")
            inp = raw_input("URI "+str(counter)+": ")
            if (inp.lower() == "done"):
                done = True
            elif (inpu == ""):
                playlists.append(PlaylistMergerClasses.Playlist(token, username, inp))
            else:
                playlists.append(PlaylistMergerClasses.Playlist(token, inpu, inp))
            counter += 1
        print("List of Merging Algorithms. Case sensetive!")
        for algorithm in MergingAlgorithms.MergingAlgorithm.__subclasses__():
            print algorithm.__name__

        algo = raw_input("Please choose an algorithm from those listed: ")
        
        print("List of Playlist Merging Algorithms. Case sensetive!")
        for algorithm in MergingAlgorithms.PlaylistMergerAlgorithm.__subclasses__():
            print algorithm.__name__
        playlist_algo = raw_input("Please choose an algorithm for merging playlists: ")
        instance.menu(instance, username, token, algo, playlist_algo, *playlists)

    inp = raw_input("Done, the new playlist is now added to your account. Type \'done\' to exit, or anything else to restart: ")
    if (inp.lower()=="done"): exit = True
