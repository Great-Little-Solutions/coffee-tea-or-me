from coffee_tea_or_me.helpers.helper import Helper


class OrderHandler:


    # Create orders file, to be used when someone starts a coffee run
    def create_orders_file(chat_id, message_id, opening_message):
        with open(Helper.file_path('orders/%s-%s.txt' % (chat_id, message_id)), 'a+') as data_file:
            data_file.write('%s\n\n' % opening_message)


    # Write to orders file
    def write_to_orders_file(chat_id, message_id, user, drink):
        with open(Helper.file_path('orders/%s-%s.txt' % (chat_id, message_id)), 'a+') as data_file:
            data_file.write('%s - %s\n' % (user, drink))


    # Update orders message in group
    def update_orders_in_group(bot, chat_id, message_id):
        with open(Helper.file_path('orders/%s-%s.txt' % (chat_id, message_id)), 'r') as data_file:
            orders = data_file.read()

        bot.edit_message_text(text=orders,
                              chat_id=chat_id,
                              message_id=message_id)
