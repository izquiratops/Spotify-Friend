import spotipy
import spotipy.util as util
import json

# Imported tokens/data from APIs
import config

def get_token():
	return util.prompt_for_user_token(username=config.app_name,\
				scope='playlist-read-collaborative playlist-modify-public',\
				client_id=config.SPOTIPY_CLIENT_ID,\
				client_secret=config.SPOTIPY_CLIENT_SECRET,\
				redirect_uri=config.SPOTIPY_REDIRECT_URI)

def create_playlist(spotify_token, playlist_name):
	sp = spotipy.Spotify(auth=spotify_token)
	sp.trace = False
	playlist = sp.user_playlist_create(config.spotify_username, playlist_name)
	with open('playlist_return.json', 'w', encoding='utf-8') as f:
		json.dump(playlist, f, indent = 4)

def show_playlists(spotify_token, spotify_username):
	sp = spotipy.Spotify(auth=spotify_token)
	playlists = sp.user_playlists(spotify_username)

	playlists_list = []
	while playlists:
		for playlist in playlists['items']:
			playlists_list.append((playlist['uri'], playlist['name']))
			# print("%s %s" % (playlist['uri'], playlist['name']))
		if playlists['next']:
			playlists = sp.next(playlists)
		else:
			playlists = None

	return playlists_list

def add_song(spotify_token, playlist_id, song_id):
	sp = spotipy.Spotify(auth=spotify_token)
	sp.trace = False
	sp.user_playlist_add_tracks(config.spotify_username, playlist_id, [song_id])