#! python3
# test_bot.py

import glob
import os
import unittest


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


if __name__ == '__main__':
    unittest.main()