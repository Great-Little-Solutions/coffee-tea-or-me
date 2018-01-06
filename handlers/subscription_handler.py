from helpers.helper import Helper

class SubscriptionHandler:


    # Add a user to coffee run subscribers for a group chat
    def add_to_subscribers(chat_id, user_id):
        with open(Helper.file_path('subscribers/%s.txt' % chat_id), 'a+') as data_file:
            for line in data_file:
                if str(user_id) in line.rstrip():
                    break
            else:  # user_id not found in current subscribers, we are at eof
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
