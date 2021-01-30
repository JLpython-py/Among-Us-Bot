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

# TODO: Uncomment once Airship map is released
# AIRSHIP = db.AirshipDB()
# AIRSHIP.execute_query(SETUP_QUERIES, "w")

MIRAHQ = db.MIRAHQDB()
MIRAHQ.execute_query(SETUP_QUERIES, "w")

POLUS = db.PolusDB()
POLUS.execute_query(SETUP_QUERIES, "w")

THESKELD = db.TheSkeldDB()
THESKELD.execute_query(SETUP_QUERIES, "w")
