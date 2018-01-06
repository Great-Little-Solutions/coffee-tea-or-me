from handlers.keyboard_handler import KeyboardHandler
from helpers.helper import Helper

class NotificationHandler:


    # Send coffee run notification to subscribers for a group
    def send_notification_to_subscribers(bot, update, message):
        with open(Helper.file_path('subscribers/%s.txt' % update.message.chat.id), 'r') as data_file:
            for line in data_file:
                bot.send_message(chat_id=line.rstrip(),
                                 text='%s volunteered to be the kopi boy/girl, order now or else...'
                                 % update.message.from_user.first_name,
                                 reply_markup=KeyboardHandler().keyboard_reply_markup(message))
