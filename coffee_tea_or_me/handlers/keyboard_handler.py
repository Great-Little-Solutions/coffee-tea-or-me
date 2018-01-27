import json
import itertools

from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from coffee_tea_or_me.helpers.helper import Helper


class KeyboardHandler:


    # Generate all drink combinations
    def generate_drink_combis(self):
        # Read drinks.json so that keyboard can be populated later
        with open(Helper.file_path('drinks.json')) as data_file:
            drinks_data = json.load(data_file)

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
    def keyboard(self, message):
        combinations = self.generate_drink_combis()

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
    def keyboard_reply_markup(self, message):
        return InlineKeyboardMarkup(self.keyboard(message))
