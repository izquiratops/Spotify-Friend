# Telegram-API
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
# Spotipy
import spotipy
import spotipy.util as util
# Imported tokens from APIs
import logging

# 'Updater' fetches new updates from telegram and passes them on to the 'Dispatcher'
# 'use_context' arg to get better backwards compatibility
updater = Updater(token=config.token, use_context=True)
dispatcher = updater.dispatcher

# 'Logging' module will let you know when (and why) things don't work as expected
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

scope = 'playlist-modify-public'


def read_message(update, context):
	if 'open.spotify.com/' in update.message.text:
		hash = update.message.text.split('/')[-1].split('?si=')[0]

read_handler = MessageHandler(Filters.text, read_message)
dispatcher.add_handler(read_handler)

updater.start_polling()