import sqlite3
from . import config
from flask import g
import random
import logging


def _get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(config.DATABASE_PATH)
        db.row_factory = sqlite3.Row
    return db

def create_database(conn, schema_file_path):
    logging.info("Creating database")
    with open(schema_file_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    logging.info("Database created")

def _query_db(query, args=(), one=False):
    cur = _get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_image_from_database(ids):
    """
    Get image from sql for ids
    If the Ids are missing, we return 10 random images
    """
    if not ids:
        ids = [random.randint(1, 1000) for _ in range(10)]
    query = "SELECT * FROM images WHERE id IN ({ids})".format(ids=",".join(map(str,ids)))
    return _query_db(query)

