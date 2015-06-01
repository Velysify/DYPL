import PlaylistMergerClasses

instance = PlaylistMergerClasses

exit = False

#test data ---------------------------------------------------------------
test_token = 'BQD1y4O7VEndT6L6R19vZvuOWuckGyvZdpmfJhdm_goRWuzPJXnIu4yTFTLK5n0P1VwaOytIs9EZQtLryKqa4SjBwh9JaR9EtuB6zp0i0jmMpfvqBzVNGYqxZ_yndNXHLuJ0ixndMoQbYD44lWUcfWv59pQOl2acPSZat4-HDyB86jDIP1nzFPfu691S-VeL0JJa4WQp5ELKz4YLqyHykc2_2xgVOgMOX4VcE519g31xt38g-NUtKlF8DWySAJTNelYRrqEayqC-NgwMwaT0t9FZlKZSWpRpkYHUMI8Uh34'
test_username = "littaly"
empty_playlist = PlaylistMergerClasses.Playlist(test_token, test_username, None)
metal_and_top40_playlist = '66bduhu9Juv1oeKvdYV4lQ'
classic_hiphop_and_rock_playlist = '0LNfNIbJBPPNt8mCM8GQ1p'
schlager_and_pop_playlist = '1GKhWgfJoDrQEnPczfNCAh'
#test data ----------------------------------------------------------------



while (not exit):
    print "Welcome to the Spotify Playlist Merger"

    username = raw_input("please enter your account username")
    token = raw_input("Please enter the access token for your account")

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
            inp = raw_input("URI "+str(counter)+": ")

            if (inp.lower() == "done"):
                done = True
            else:
                playlist_uris.append(inp)


        instance.menu(instance, username, token, *playlist_uris)

    inp = raw_input("Done, the new playlist is added to your account. Type \'done\' to exit, or anything else to restart")
    if (inp.lower()=="done"): exit = True
