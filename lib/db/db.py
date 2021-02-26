#! python3
# db.py

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

import os
import sqlite3


class DBConnection:
    """ Connect to data/db/db.sqlite
"""
    def __init__(self, database):
        self.connection = sqlite3.connect(
            os.path.join('data', 'db', database)
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """ Close database connection
"""
        self.connection.close()

    def write_query(self, query, *args):
        self.cursor.execute(query, tuple(args))
        self.connection.commit()

    def read_query(self, query, *args):
        self.cursor.execute(query, tuple(args))
        values = self.cursor.fetchall()
        return values

    def read_columns(self):
        values = [
            d[0] for d in self.cursor.description
        ]
        return values


class AirshipDB(DBConnection):
    """ Connect to data/db/airship.sqlite
"""
    def __init__(self):
        super().__init__(
            database="airship.sqlite"
        )


class MIRAHQDB(DBConnection):
    """ Connect to data/db/airship.sqlite
"""
    def __init__(self):
        super().__init__(
            database="mira_hq.sqlite"
        )


class PolusDB(DBConnection):
    """ Connect to data/db/airship.sqlite
"""
    def __init__(self):
        super().__init__(
            database="polus.sqlite"
        )


class TheSkeldDB(DBConnection):
    """ Connect to data/db/airship.sqlite
"""
    def __init__(self):
        super().__init__(
            database="the_skeld.sqlite"
        )
