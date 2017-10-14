import json
import logging

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def keyboard():
    keyboard = [[InlineKeyboardButton('Kopi', callback_data='Kopi'),
                    InlineKeyboardButton('Teh', callback_data='Teh')],
                [InlineKeyboardButton('Kopi-O', callback_data='Kopi-O'),
                    InlineKeyboardButton('Teh-O', callback_data='Teh-O')]]
    return keyboard

def keyboard_reply_markup():
    return InlineKeyboardMarkup(keyboard())

def start(bot, update):
    update.message.reply_text('%s started the coffee run, please order:' % update.message.from_user.first_name,
                              reply_markup = keyboard_reply_markup())


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text = "%s\n%s selected option: %s" % (query.message.text, query.from_user.first_name, query.data),
                          chat_id = query.message.chat_id,
                          message_id = query.message.message_id,
                          reply_markup = keyboard_reply_markup())


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


with open('config.json') as data_file:
    data = json.load(data_file)

updater = Updater(token=data['bot_token'])

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)

updater.start_polling()

updater.idle()
