#! python3
# test_cogs.py

import unittest
from urllib.request import urlopen


class TestInfoCog(unittest.TestCase):

    def test_command_addresses(self):
        urls = [
            "https://github.com/JLpython-py/Among-Us-Bot",
            "https://github.com/JLpython-py/Among-Us-Bot/wiki",
            "https://github.com/JLpython-py/AmongUsData/",
            "https://jlpython-py.github.io/Among-Us-Bot/",
            "https://github.com/JLpython-py/Among-Us-Bot/issues/new/choose",

        ]
        for url in urls:
            self.assertEqual(urlopen(url).getcode(), 200)


class TestMapDatabaseCog(unittest.TestCase):
    pass


class TestRandomAmongUsCog(unittest.TestCase):
    pass


class TestVoiceChannelControlCog(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
