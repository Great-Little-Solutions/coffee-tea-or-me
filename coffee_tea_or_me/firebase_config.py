import pyrebase
import json

from coffee_tea_or_me.helpers.helper import Helper

def read_config_file():
    with open(Helper.file_path('firebase_config.json')) as config_file:
        config = json.load(config_file)
    return config


firebase = pyrebase.initialize_app(read_config_file())
db = firebase.database()
