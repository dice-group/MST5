import unittest
from generate_train_csv import *

class Test_generate_train_csv(unittest.TestCase):
    def test_get_only_supported_languages(self):
        languages = ['en', 'de', 'br', 'ar']
        languages = get_only_supported_languages(languages)
        self.assertTrue('en' in languages)
        self.assertFalse('ar' in languages)


if __name__ == '__main__':
    unittest.main()
