import json
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

# Enable logging to help with debugging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Handler for /start command
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm a bot, please talk to me!")


# Handler for messages without recognisable commands
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


# Read config file to get telegram bot token later
with open('config.json') as data_file:
    data = json.load(data_file)

# Updater receives updates from Telegram server and deliver to dispatcher
updater = Updater(token=data['bot_token'])

# Dispatcher handles the updates, and dispatches them to the handlers
dispatcher = updater.dispatcher


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

updater.start_polling()

updater.idle()
