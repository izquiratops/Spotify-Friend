# Telegram-API
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import spoty, config, json

def help(update, context):
	message = "List of commands:\n/create_playlist\n/get_link\n\n(I'm not gonna explain this shit, this is so self-explanatory)"
	update.message.reply_text(message)

def create_playlist(update, context):
	ret = spoty.show_playlists(spotify_token, config.spotify_username)
	exist = False

	for playlist in ret:
		if config.playlist_name == playlist[1]:
			message, exist = 'Already been created', True
	if not exist:
		spoty.create_playlist(spotify_token, config.playlist_name)
		message = config.playlist_name + ' created successfully!'

	context.bot.send_message(chat_id=update.message.chat_id, text=message)

def get_link(update, context):
	with open('playlist_return.json') as file:
		data = json.load(file)
		message = data['external_urls']['spotify']

	if message:
		context.bot.send_message(chat_id=update.message.chat_id, text=message)

def read_message(update, context):
	if 'open.spotify.com/' in update.message.text:
		song_id = update.message.text.split('/')[-1].split('?si=')[0]
	else:
		return

	ret = spoty.show_playlists(spotify_token, config.spotify_username)
	for playlist in ret:
		# playlist es un tuple de (ID, Name)
		if config.playlist_name == playlist[1]:
			spoty.add_song(spotify_token, playlist[0], song_id)

# 'Updater' fetches new updates from telegram and passes them on to the 'Dispatcher'
# 'use_context' arg to get better backwards compatibility
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher

# 'Logging' module will let you know when (and why) things don't work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

spotify_token = spoty.get_token()

dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('create_playlist', create_playlist))
dispatcher.add_handler(CommandHandler('get_link', get_link))
dispatcher.add_handler(MessageHandler(Filters.text, read_message))

updater.start_polling()
updater.idle()