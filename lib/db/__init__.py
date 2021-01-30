#! python3
# lib.db.__init__.py

"""
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
