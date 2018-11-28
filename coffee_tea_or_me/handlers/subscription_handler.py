from coffee_tea_or_me.helpers.helper import Helper
import os

class SubscriptionHandler:


    # Add a user to coffee run subscribers for a group chat
    def add_to_subscribers(chat_id, user_id):
        if os.path.exists(Helper.file_path('subscribers/%s.txt' % chat_id)):
            with open(Helper.file_path('subscribers/%s.txt' % chat_id), 'r') as data_file:
                for line in data_file:
                    if str(user_id) in line.rstrip():
                        return

        with open(Helper.file_path('subscribers/%s.txt' % chat_id), 'a+') as data_file:
            data_file.write(str(user_id) + '\n')


    # Remove a user from coffee run subscribers from a group chat
    def remove_from_subscribers(chat_id, user_id):
        file = open(Helper.file_path('subscribers/%s.txt' % chat_id), 'r')
        lines = file.readlines()
        file.close()

        file = open(Helper.file_path('subscribers/%s.txt' % chat_id), 'w')
        for line in lines:
            if line.rstrip() != str(user_id):
                file.write(line)
        file.close()
