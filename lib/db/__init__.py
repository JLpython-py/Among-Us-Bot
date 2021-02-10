#! python3
# lib.db.__init__.py

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

from . import db

SETUP_QUERIES = [
    """CREATE TABLE IF NOT EXISTS actions (
    name text PRIMARY KEY,
    type text,
    rooms text,
    severity text
    );""",
    """CREATE TABLE IF NOT EXISTS locations (
    name text PRIMARY KEY,
    connections text,
    vents text,
    tasks text,
    actions text
    );""",
    """CREATE TABLE IF NOT EXISTS maps (
    name text PRIMARY KEY
    );""",
    """CREATE TABLE IF NOT EXISTS tasks (
    name text PRIMARY KEY,
    type text,
    room text,
    steps text,
    description text
    );""",
    """CREATE TABLE IF NOT EXISTS vents (
    name text PRIMARY KEY,
    connections text
    );"""
    ]

AIRSHIP = db.AirshipDB()
MIRAHQ = db.MIRAHQDB()
POLUS = db.PolusDB()
THESKELD = db.TheSkeldDB()

CONNECTIONS = [AIRSHIP, MIRAHQ, POLUS, THESKELD]
for CONN in CONNECTIONS:
    for QUERY in SETUP_QUERIES:
        CONN.execute_query(QUERY, "w")
