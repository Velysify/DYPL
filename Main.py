import PlaylistMergerClasses

instance = PlaylistMergerClasses

exit = False

#test data ---------------------------------------------------------------
test_token = 'BQDUXmqKsWSLlT26sC7PDUdJSUCKSMZce6TWa53WnryRwgv_9jD86U3ELu6BV1V-dzH1o7SuGAmn9eSLdhdty_jbE0Qgm7qUBel6i5BkTJTRBKom-gu6KUzuHZw8ta76eykfYw2qxhSb57_goGSZBXf35fGPuWFcF6BPd-jM7mEB32qaqSL9r-N_zMjQFQlLhrtnB1nlbntPsEhNfSIaSfoIzgMus1keSgFRLdoWz9GwVGy_'
test_username = "velys"
metal_and_top40_playlist = '7n0np8taZhlvE0iNYjC9Gu'
classic_hiphop_and_rock_playlist = '3jeoIpQpRdDrPskLdcRVW0'
schlager_and_pop_playlist = '0FK7E35FEHnvIGZZeN6wqG'
#test data ----------------------------------------------------------------



while (not exit):
    print "Welcome to the Spotify Playlist Merger"

    username = raw_input("Please enter your account username: ")
    token = raw_input("Please enter the access token for your account: ")

    done = False
    counter = 1
    playlist_uris = []
    inpp = raw_input("Now enter the URIs of the playlists you wish to merge, type \'done\' when you're done, '\test'\ to run with default testdata or anything else to proceed")

    if (inpp.lower() == "done"):
        exit = True
    elif (inpp.lower() == "test"):
        instance.menu(instance, test_username, test_token, metal_and_top40_playlist, classic_hiphop_and_rock_playlist, schlager_and_pop_playlist)
    else:

        while (not done):
            inpu = raw_input("Please enter the username for the next playlist: ")
            inp = raw_input("URI "+str(counter)+": ")
            if (inp.lower() == "done"):
                done = True
            elif (inpu == ""):
                playlists.append(PlaylistMergerClasses.Playlist(token, username, inp))
            else:
                playlists.append(PlaylistMergerClasses.Playlistt(token, inpu, inp))



        instance.menu(instance, username, token, *playlists)

    inp = raw_input("Done, the new playlist is not added to your account. Type \'done\' to exit, or anything else to restart")
    if (inp.lower()=="done"): exit = True
