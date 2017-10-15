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


# Restrict to groups
def not_a_group(update):
    if update.message.chat.type == 'private':
        update.message.reply_text('You can only do this in groups.')
        return True

    return False


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
def keyboard(message):
    combinations = generate_drink_combis()

    keyboard = [[InlineKeyboardButton('Kopi',
                                      callback_data='%s:%s:Kopi' % (
                                          message.chat.id,
                                          message.message_id)),
                 InlineKeyboardButton('Teh',
                                      callback_data='%s:%s:Teh' % (
                                          message.chat.id,
                                          message.message_id))]]

    for i in range(0, len(combinations), 2):
        left_item = combinations[i]
        keyboard_item = [InlineKeyboardButton(left_item,
                         callback_data='%s:%s:%s' % (message.chat.id,
                                                     message.message_id,
                                                     left_item))]

        right_item = []
        if i + 1 < len(combinations):
            right_item = combinations[i + 1]
            keyboard_item.append(InlineKeyboardButton(right_item,
                                 callback_data='%s:%s:%s' % (
                                     message.chat.id,
                                     message.message_id,
                                     right_item)))

        keyboard.append(keyboard_item)

    return keyboard


# Generate the inline keyboard markup for keyboard
def keyboard_reply_markup(message):
    return InlineKeyboardMarkup(keyboard(message))


# Send coffee run notification to subscribers for a group
def send_notification_to_subscribers(bot, update, message):
    with open('subscribers/%s.txt' % update.message.chat.id, 'r') as data_file:
        for line in data_file:
            bot.send_message(chat_id=line.rstrip(),
                             text='%s started the coffee run, please order:'
                             % update.message.from_user.first_name,
                             reply_markup=keyboard_reply_markup(message))


# Handler for /start command
def start(bot, update):
    if not_a_group(update):
        return

    message = update.message.reply_text('%s started the coffee run, please order via the notification sent to you privately. Use /sub to subscribe to future notifications. Current orders:' % update.message.from_user.first_name)
    send_notification_to_subscribers(bot, update, message)


# Write to orders file
def write_to_orders_file(chat_id, message_id, user, drink):
    with open('orders/%s-%s.txt' % (chat_id, message_id), 'w+') as data_file:
        data_file.write('%s - %s\n' % (user, drink))


# Update orders message in group
def update_orders_in_group(bot, chat_id, message_id):
    with open('orders/%s-%s.txt' % (chat_id, message_id), 'r') as data_file:
        orders = data_file.read()

    bot.edit_message_text(text=orders,
                          chat_id=chat_id,
                          message_id=message_id)


# Handler for button click callbacks
def button(bot, update):
    query = update.callback_query
    callback_data = query.data.split(':')
    chat_id_for_editing = callback_data[0]
    message_id_for_editing = callback_data[1]
    drink = callback_data[2]

    write_to_orders_file(chat_id_for_editing,
                         message_id_for_editing,
                         query.from_user.first_name,
                         drink)

    update_orders_in_group(bot, chat_id_for_editing, message_id_for_editing)

    # Update private chat
    bot.edit_message_text(text="You selected option: %s" % drink,
                          chat_id=query.message.chat.id,
                          message_id=query.message.message_id)


# Add a user to coffee run subscribers for a group chat
def add_to_subscribers(chat_id, user_id):
    with open('subscribers/%s.txt' % chat_id, 'w+') as data_file:
        for line in data_file:
            if str(user_id) in line.rstrip():
                break
        else:  # user_id not found in current subscribers, we are at eof
            data_file.write(str(user_id) + '\n')


# Remove a user from coffee run subscribers from a group chat
def remove_from_subscribers(chat_id, user_id):
    file = open('subscribers/%s.txt' % chat_id, 'r')
    lines = file.readlines()
    file.close()

    file = open('subscribers/%s.txt' % chat_id, 'w')
    for line in lines:
        if line.rstrip() != str(user_id):
            file.write(line)
    file.close()


# Handler for /sub command
def sub(bot, update):
    if not_a_group(update):
        return

    add_to_subscribers(update.message.chat.id,
                       update.message.from_user.id)

    update.message.reply_text('%s has subscribed to coffee runs. You will receive a notification from yours truly when a coffee run starts in group: %s. Click here @%s and press START so that I can send you notifications. Delete that chat and you will never hear from me again.' % (update.message.from_user.first_name, update.message.chat.title, bot.get_me().username))


# Handler for /unsub comand
def unsub(bot, update):
    if not_a_group(update):
        return

    remove_from_subscribers(update.message.chat.id,
                            update.message.from_user.id)

    update.message.reply_text('%s has unsubscribed from coffee runs. You will no longer receive notifications from yours truly when a coffee run starts in group: %s' % (update.message.from_user.first_name, update.message.chat.title))


# Handler for /help command
def help(bot, update):
    update.message.reply_text('/start to start a coffee run\n' +
                              '/sub in group chats to subscribe ' +
                              'to coffee run notifications' +
                              '\n/unsub to do the opposite of /sub')


# Handler to log errors
def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


# Read config file to get telegram bot token later
with open('config.json') as data_file:
    config_data = json.load(data_file)

updater = Updater(token=config_data['bot_token'])

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('sub', sub))
updater.dispatcher.add_handler(CommandHandler('unsub', unsub))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)

updater.start_polling()

updater.idle()
