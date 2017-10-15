import json
import logging
import itertools

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler

# Enable logging to help with debugging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Read drinks.json so that keyboard can be populated later
with open('drinks.json') as data_file:
    drinks_data = json.load(data_file)


# Generate all drink combinations
def generate_drink_combis():
    drinks = drinks_data['0']
    combinations = []

    for i in range(1, 5):
        iterables = [drinks]

        for j in range(1, i + 1):
            iterables.append(drinks_data[str(j)])

        for combination in itertools.product(*iterables):
            combinations.append('-'.join(combination))

    return combinations


# Populate the keyboard with drinks and options
def keyboard():
    combinations = generate_drink_combis()

    keyboard = [[InlineKeyboardButton('Kopi', callback_data='Kopi'),
                 InlineKeyboardButton('Teh', callback_data='Teh')]]

    for i in range(0, len(combinations), 2):
        left_item = combinations[i]
        keyboard_item = [InlineKeyboardButton(left_item,
                         callback_data=left_item)]

        right_item = []
        if i + 1 < len(combinations):
            right_item = combinations[i + 1]
            keyboard_item.append(InlineKeyboardButton(right_item,
                                 callback_data=right_item))

        keyboard.append(keyboard_item)

    return keyboard


# Generate the inline keyboard markup for keyboard
def keyboard_reply_markup():
    print(InlineKeyboardMarkup(keyboard()))
    return InlineKeyboardMarkup(keyboard())


# Handler for /start command
def start(bot, update):
    update.message.reply_text('%s started the coffee run, please order:' % update.message.from_user.first_name,
                              reply_markup=keyboard_reply_markup())


# Handler for button click callbacks
def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="%s\n%s selected option: %s" % (query.message.text, query.from_user.first_name, query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=keyboard_reply_markup())


# Handler for /help command
def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


# Handler to log errors
def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


# Read config file to get telegram bot token later
with open('config.json') as data_file:
    config_data = json.load(data_file)

updater = Updater(token=config_data['bot_token'])

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)

updater.start_polling()

updater.idle()
