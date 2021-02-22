#! python3
# functional_tests.py

"""
==============================================================================
MIT License

Copyright (c) 2020 Jacob Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
==============================================================================
"""

import asyncio
import os
import unittest

from lib.bot import BotRoot
from lib.db import db


class TestBotDatabaseInteraction(unittest.TestCase):

    def setUp(self):
        self.bot = BotRoot()
        self.conns = {
            "airship": self.bot.airship, "mirahq": self.bot.mirahq,
            "polus": self.bot.polus, "theskeld": self.bot.theskeld
        }

    def tearDown(self):
        self.bot.airship.close_connection()
        self.bot.mirahq.close_connection()
        self.bot.polus.close_connection()
        self.bot.theskeld.close_connection()

    def test_all(self):
        self.assertTrue(
            all([self.bot.airship, self.bot.mirahq, self.bot.polus,
                 self.bot.theskeld])
        )

        maps = ["mirahq", "polus", "theskeld"]
        tables = ["actions", "locations", "maps", "tasks", "vents"]

        for mapname in maps:
            for table in tables:
                query = f"""
                SELECT *
                FROM {table}
                """
                content = self.conns[mapname].read_query(query)
                self.assertTrue(content)
                self.assertTrue(
                    os.path.exists(
                        os.path.join("data", mapname, table)
                    )
                )
                columns = self.conns[mapname].read_columns()
                for row in content:
                    name = dict(zip(columns, row))['name']
                    self.assertTrue(
                        os.path.exists(
                            os.path.join(
                                "data", mapname, table, f"{name}.png"
                            )
                        ),
                        (mapname, table, name)
                    )


if __name__ == '__main__':
    unittest.main()
