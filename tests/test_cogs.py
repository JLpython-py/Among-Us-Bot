#! python3
# test_cogs.py

import json
import os
import sqlite3
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

    def test_database_paths(self):
        databases = [
            "airship.sqlite", "mira_hq.sqlite", "polus.sqlite",
            "the_skeld.sqlite"
        ]
        for dbpath in databases:
            self.assertTrue(
                os.path.exists(os.path.join("data", "db", dbpath)),
                dbpath
            )

    def test_database_tables(self):
        databases = [
            "airship.sqlite", "mira_hq.sqlite", "polus.sqlite",
            "the_skeld.sqlite"
        ]
        tables = [
            "actions", "locations", "maps", "tasks", "vents"
        ]
        for db in databases:
            connection = sqlite3.connect(
                os.path.join("data", "db", db)
            )
            cursor = connection.cursor()
            for tab in tables:
                query = f"""
                SELECT *
                FROM {tab}
                """
                cursor.execute(query)
                self.assertTrue(cursor.fetchall())
            connection.close()

    def test_search_command_emojis(self):
        emojis = {
            u'\u23ee': '⏮', u'\u23ea': '⏪', u'\u25c0': '◀', u'\u25b6': '▶',
            u'\u23e9': '⏩', u'\u23ed': '⏭', u'\u2714': '✔', u'\u274c': '❌'
        }
        for emoji in emojis:
            self.assertEqual(emoji, emojis[emoji])


class TestRandomAmongUsCog(unittest.TestCase):

    def test_settings_file_path(self):
        self.assertTrue(
            os.path.exists(os.path.join("data", "settings.txt"))
        )

    def test_settings_file_contents(self):
        with open(os.path.join("data", "settings.txt")) as file:
            data = json.load(file)
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 16)
        self.assertTrue(
            all([isinstance(k, str) for k in data])
        )
        self.assertTrue(
            all([isinstance(v, list) for v in data.values()])
        )
        self.assertTrue(
            all([isinstance(i, str) or isinstance(i, int)
                 for v in data.values() for i in v])
        )

    def test_map_logo_images_path(self):
        maps = ["Airship", "MIRA HQ", "Polus", "The Skeld"]
        self.assertTrue(
            all([os.path.exists(
                os.path.join(
                    "data",
                    f"{''.join(m.lower().split())}.png"
                )
            ) for m in maps])
        )


class TestVoiceChannelControlCog(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
