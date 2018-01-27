import unittest
from coffee_tea_or_me.firebase_config import read_config_file


class TestFirebaseConfig(unittest.TestCase):

    def test_read_config_file(self):
        expected_keys = ['apiKey', 'authDomain', 'databaseURL', 'storageBucket', 'serviceAccount']
        self.assertEqual(list(read_config_file().keys()), expected_keys)


if __name__ == '__main__':
    unittest.main()
