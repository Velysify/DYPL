import spotipy

baseball_uri = 'spotify:artist:2HMtMLKEIOoamQysJlFP7i'
spotify = spotipy.Spotify()

results = spotify.artist_albums(lbc_uri, album_type='album')
albums = results['items']
while results['next']:
	results = spotify.next(results)
	albums.extend(results['items'])

for album in albums:
        trackresult = spotify.album_tracks(album['id'])
        tracks = trackresult['items']
        while trackresult['next']:
                trackresult = spotify.next(trackresult)
                tracks.extend(trackresult['items'])
        for track in tracks:
                print(track['name'])
