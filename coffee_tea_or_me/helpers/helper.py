import os

global ROOT_DIR
ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)


class Helper:


    # Restrict to groups
    def not_a_group(update):
        if update.message.chat.type == 'private':
            update.message.reply_text('You can only do this in groups.')
            return True

        return False


    def not_authorised(update):
        authorised_people = ['shermanelee', 'ngjhalex', 'stanlylau']

        return update.message.from_user.username not in authorised_people


    def file_path(file):
        print('---------------------------')
        print(file)
        print(ROOT_DIR)
        print(os.path.join(ROOT_DIR, file))
        print('---------------------------')
        return os.path.join(ROOT_DIR, file)
