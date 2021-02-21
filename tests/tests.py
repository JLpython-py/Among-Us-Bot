#! python3
# tests.py

import glob
import os
import unittest
from urllib.request import urlopen


class TestBotINIT(unittest.TestCase):

    def test_cogs_directory_exists(self):
        self.assertTrue(
            os.path.exists(os.path.join('lib', 'cogs'))
        )

    def test_navigate_cogs_directory(self):
        cogs = [
            "info.py", "mapdatabase.py", "randomamongus.py",
            "voicechannelcontrol.py"
        ]
        pyfiles = [
            f for f in os.listdir(os.path.join('lib', 'cogs'))
            if os.path.splitext(f)[1] == ".py"
        ]
        self.assertEqual(cogs, pyfiles)

    def test_glob_pattern(self):
        pattern = "lib/cogs/*.py"
        paths = [
            os.path.split(os.path.normpath(p))[1]
            for p in glob.glob(pattern)
        ]
        files = [
            f for f in os.listdir(os.path.join('lib', 'cogs'))
            if os.path.splitext(f)[1] == ".py"
        ]
        self.assertEqual(set(paths), set(files))


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


if __name__ == '__main__':
    unittest.main()
