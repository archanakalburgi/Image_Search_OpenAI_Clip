import imp
import pytest
import main_app
from src import db_util
import sqlite3
from src import config
import os
import shutil

@pytest.fixture
def app():
    app = main_app.create_app()
    return app


@pytest.fixture()
def connection():
    os.makedirs("tests/cache/") # may be use tempfiles
    config.ANNOY_INDEX_PATH = "tests/cache/test.ann"
    config.DATABASE_PATH = "tests/cache/test.db"
    conn = sqlite3.connect(config.DATABASE_PATH)
    # conn.row_factory = sqlite3.Row
    db_util.create_database(conn, config.SQL_SCRIPT_PATH)
    yield conn
    conn.close()
    shutil.rmtree("tests/cache/")