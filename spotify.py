# Spotipy
import spotipy
import spotipy.util as util

import config

config.set_exports()
scope = 'playlist-modify-private'
token = util.prompt_for_user_token(config.client_username, scope, config.SPOTIPY_CLIENT_ID, config.SPOTIPY_CLIENT_SECRET, config.SPOTIPY_REDIRECT_URI)

if token:
	sp = spotipy.Spotify(auth=token)
	sp.trace = False
	playlists = sp.user_playlist_create(config.client_username,\
			'playlist_name', 'playlist_description')
	print(playlists)