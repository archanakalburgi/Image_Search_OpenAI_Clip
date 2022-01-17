import os

import sqlite3
import src.config as config
from src import db_util
from datetime import datetime
import shutil
import logging


"""
This is a helper script for developer. Not intended for production use.
Script is useful to clean everything up and start fresh.
Warning: Will move database, images and annoy index to backup folder.
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def _get_database_connection(database_path):
    conn = sqlite3.connect(database_path)
    return conn


def _date_suffix():  # TODO test this
    back_folder_date = datetime.now().strftime("%Y_%m_%d")
    back_folder_hour = datetime.now().strftime(
        "%M"
    )  # TODO: change this to %H after testing
    return back_folder_date + "/" + back_folder_hour


def _backup_path(asset):  # TODO test this
    backup_path = os.path.join(config.BACK_UP_PATH + "/" + asset + "/", _date_suffix())
    return backup_path


def _if_file_exists_backup(file_or_dir, asset):
    """
    asset - db file or annoy index or images
    """

    if os.path.exists(file_or_dir):
        backup_path = _backup_path(asset)
        logging.info(f"Backing up {asset} to {backup_path}")
        os.makedirs(f"{backup_path}", exist_ok=True)
        try:
            shutil.move(
                file_or_dir, backup_path
            )  # If the samefile exists, it will be overwritten.?
            logging.info(f"Backup {file_or_dir} to {backup_path} successful")
            return
        except shutil.Error as e:
            logging.error(f"Could not move {file_or_dir} to {backup_path} - {e}")
    else:
        logging.info(f"{file_or_dir} does not exist. Nothing to backup")
        return


def main():
    """
    Please make sure config.py is set up correctly.
    """
    logging.info("Starting data pipeline")
    os.makedirs(config.CACHE_DIR, exist_ok=True)
    os.makedirs(config.MODEL_DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(config.IMAGES_UPLOAD_PATH, exist_ok=True)
    _if_file_exists_backup(config.DATABASE_PATH, "database")
    _if_file_exists_backup(config.ANNOY_INDEX_PATH, "database")
    conn = _get_database_connection(config.DATABASE_PATH)
    db_util.create_database(conn, config.SQL_SCRIPT_PATH)
    return

if __name__ == "__main__":
    main()
