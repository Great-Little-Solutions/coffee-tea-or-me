import glob
import os
import re

from coffee_tea_or_me.helpers.helper import Helper


class OrderHandler:

    # Create orders file, to be used when someone starts a coffee run
    def create_orders_file(chat_id, message_id, opening_message):
        with open(Helper.file_path('orders/%s-%s.txt' % (chat_id, message_id)), 'a+') as data_file:
            data_file.write('%s\n\n' % opening_message)

    # Write to orders file
    def write_to_orders_file(chat_id, message_id, user, drink):
        order_count = 0
        for line in open(Helper.file_path('orders/%s-%s.txt' % (chat_id, message_id)), 'r'):
            if ' - ' in line:
                order_count += 1

        order_count += 1

        with open(Helper.file_path('orders/%s-%s.txt' % (chat_id, message_id)), 'a+') as data_file:
            data_file.write('%d. %s - %s\n' % (order_count, user, drink))

    # Update orders message in group
    def update_orders_in_group(bot, chat_id, message_id):
        with open(Helper.file_path('orders/%s-%s.txt' % (chat_id, message_id)), 'r') as data_file:
            orders = data_file.read()

        bot.edit_message_text(text=orders,
                              chat_id=chat_id,
                              message_id=message_id)

    def update_done_order(bot, chat_id, item_num):
        list_of_orders_in_chat = glob.glob(Helper.file_path('orders/%s-*.txt' % (chat_id)))
        latest_order_file = max(list_of_orders_in_chat, key=os.path.getctime)

        row_to_find = str(item_num) + '.'

        final_order_message = ''
        with open(latest_order_file, 'r') as data_file:
            for line in data_file:
                if line.startswith(row_to_find):
                    line = line.rstrip() + ' [done]\n'

                final_order_message = final_order_message + line

        with open(latest_order_file, 'w') as data_file:
            data_file.write(final_order_message)

        message_id = re.search('(\d+)\.txt', latest_order_file)[1]

        bot.edit_message_text(text=final_order_message,
                              chat_id=chat_id,
                              message_id=message_id)
