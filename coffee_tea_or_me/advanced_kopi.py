import sys
sys.path.append('../')

import os
import json
import logging

from coffee_tea_or_me.handlers.notification_handler import NotificationHandler
from coffee_tea_or_me.handlers.subscription_handler import SubscriptionHandler
from coffee_tea_or_me.handlers.order_handler import OrderHandler
from coffee_tea_or_me.helpers.helper import Helper

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler

# Enable logging to help with debugging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Handler for /start command
def start(bot, update):
    if Helper.not_a_group(update) or Helper.not_authorised(update):
        return

    # message = update.message.reply_text('%s volunteered to be the kopi boy/girl, please order via the notification sent to you privately. Use /sub to subscribe to future notifications. Order now or else...' % update.message.from_user.first_name)
    message = update.message.reply_text("Stanly's Coffee is now open! Please order via the notification sent to you privately. Use /sub to subscribe to future notifications.")
    OrderHandler.create_orders_file(message.chat.id, message.message_id, message.text)

    NotificationHandler.send_notification_to_subscribers(bot, update, message)


# Handler for button click callbacks
def button(bot, update):
    query = update.callback_query
    callback_data = query.data.split(':')
    chat_id_for_editing = callback_data[0]
    message_id_for_editing = callback_data[1]
    drink = callback_data[2]

    OrderHandler.write_to_orders_file(chat_id_for_editing,
                         message_id_for_editing,
                         query.from_user.first_name,
                         drink)

    OrderHandler.update_orders_in_group(bot, chat_id_for_editing, message_id_for_editing)

    # Update private chat
    bot.edit_message_text(text="You selected option: %s" % drink,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id)


# Handler for /help command
def help(bot, update):
    update.message.reply_text('/start to start a coffee run\n' +
                              '/sub in group chats to subscribe ' +
                              'to coffee run notifications' +
                              '\n/unsub to do the opposite of /sub')


# Handler to log errors
def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))



# Handler for /sub command
def sub(bot, update):
    if Helper.not_a_group(update):
        return

    SubscriptionHandler.add_to_subscribers(update.message.chat.id,
                       update.message.from_user.id)

    update.message.reply_text('%s has subscribed to coffee runs. You will receive a notification from yours truly when a coffee run starts in group: %s.\n\nClick here @%s and press "Send Message" > "START" so that I can send you notifications. Delete that chat and you will never hear from me again \U0001F608' % (update.message.from_user.first_name, update.message.chat.title, bot.get_me().username))


# Handler for /unsub comand
def unsub(bot, update):
    if Helper.not_a_group(update):
        return

    SubscriptionHandler.remove_from_subscribers(update.message.chat.id,
                            update.message.from_user.id)

    update.message.reply_text('%s has unsubscribed from coffee runs \U0001F612 One less drink to buy when kopi run starts in group: %s' % (update.message.from_user.first_name, update.message.chat.title))


def done(bot, update, args):
    if Helper.not_a_group(update) or Helper.not_authorised(update):
        return

    OrderHandler.update_done_order(bot, update.message.chat.id, int(args[0]))


# Read config file to get telegram bot token later
with open('config.json') as data_file:
    config_data = json.load(data_file)

updater = Updater(token=config_data['bot_token'])

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('sub', sub))
updater.dispatcher.add_handler(CommandHandler('unsub', unsub))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('done', done, pass_args=True))
updater.dispatcher.add_error_handler(error)

updater.start_polling()

updater.idle()
