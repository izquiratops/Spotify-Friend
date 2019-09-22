import spotipy
import spotipy.util as util
import json

# Imported tokens/data from APIs
import config

def create_playlist(spotify_token, playlist_name):
	sp = spotipy.Spotify(auth=spotify_token)
	sp.trace = False
	playlist = sp.user_playlist_create(config.spotify_username, playlist_name)
	with open('playlist_return.json', 'w', encoding='utf-8') as f:
		json.dump(playlist, f, indent = 4)

def get_playlists(spotify_token, spotify_username):
	sp = spotipy.Spotify(auth=spotify_token)
	sp.trace = False
	playlists = sp.user_playlists(spotify_username)

	playlists_list = []
	while playlists:
		for i, playlist in enumerate(playlists['items']):
			playlists_list.append((playlist['uri'], playlist['name']))
			print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'], playlist['name']))
		if playlists['next']:
			playlists = sp.next(playlists)
		else:
			playlists = None

	return playlists_list