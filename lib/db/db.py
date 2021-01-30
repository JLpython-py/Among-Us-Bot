#! python3
# db.py

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

    def execute_query(self, query, mode, *args):
        """ Pass the given query to the cursor under the determined mode
"""
        mode = mode.lower()
        if mode == "w":
            self.cursor.execute(query, tuple(args))
            self.connection.commit()
            values = []
        elif mode == "r":
            self.cursor.execute(query, tuple(args))
            values = self.cursor.fetchall()
        elif mode == "rr":
            self.cursor.execute(query, tuple(args))
            values = [
                [d[0] for d in self.cursor.description],
                self.cursor.fetchall()
            ]
        else:
            values = []
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
