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


    def file_path(file):
        print('---------------------------')
        print(file)
        print(ROOT_DIR)
        print(os.path.join(ROOT_DIR, file))
        print('---------------------------')
        return os.path.join(ROOT_DIR, file)
