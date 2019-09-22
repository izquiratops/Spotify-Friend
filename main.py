# Telegram-API
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
# Spotipy
import spotipy
import spotipy.util as util
import spotify_manager
# Imported tokens/data from APIs
import config

# 'Updater' fetches new updates from telegram and passes them on to the 'Dispatcher'
# 'use_context' arg to get better backwards compatibility
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher

# 'Logging' module will let you know when (and why) things don't work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

spotify_token = util.prompt_for_user_token(username=config.app_name,\
	scope='playlist-read-collaborative playlist-modify-public', client_id=config.SPOTIPY_CLIENT_ID,\
	client_secret=config.SPOTIPY_CLIENT_SECRET, redirect_uri=config.SPOTIPY_REDIRECT_URI)

def create_playlist(update, context):
	spotify_manager.create_playlist(spotify_token, config.playlist_name)

def read_message(update, context):
	if 'open.spotify.com/' in update.message.text:
		hash = update.message.text.split('/')[-1].split('?si=')[0]

	playlists_list = spotify_manager.get_playlists(spotify_token, config.spotify_username)
	for playlist in playlists_list:
		if config.playlist_name in playlist[1]:
			context.bot.send_message(chat_id=update.message.chat_id, text=playlist[1])

start_handler = CommandHandler('create_playlist', create_playlist)
read_handler = MessageHandler(Filters.text, read_message)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(read_handler)

updater.start_polling()