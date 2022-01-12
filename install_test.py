import os

import sqlite3
import src.config as config
from datetime import datetime
import shutil

import logging

# logging.basicConfig(filename='data_pipeline.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

def _get_database_connection(database_path):
    conn = sqlite3.connect(database_path)
    return conn


def _create_database(conn, schema_file_path):
    logging.info("Creating database")
    with open(schema_file_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    logging.info("Database created")


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

    # if os.path.exists(file_path):
    #     os.makedirs(f"{file_path}.bak", exist_ok=True)
    #     shutil.copy(file_path, file_path + ".bak")
    #     logging.info(f"{file_path} exists, backing up to {file_path}.bak")


def main():
    """
    Please make sure config.py is set up correctly.
    """
    logging.info("Starting data pipeline")
    _if_file_exists_backup(config.DATABASE_PATH, "database")
    _if_file_exists_backup(config.IMAGES_UPLOAD_PATH, "images")
    # _if_file_exists_backup(config.IMAGES_PROCESSED_PATH, "images-processed")
    conn = _get_database_connection(config.DATABASE_PATH)
    _create_database(conn, config.SQL_SCRIPT_PATH)
    return


if __name__ == "__main__":
    main()
