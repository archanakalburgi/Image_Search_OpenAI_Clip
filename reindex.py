"""
Script is used to updated the existing database with new images.
scans the config.IMAGE_FOLDER_PATH and adds any new images that where uploads.


Assumptions:
The filename for the images is assumed to be unique.(The controller that handled uploaded might need to be updated to check for duplication.)
"""

from src import annoy_reindex
import os
import logging
import shutil
from src import config
import glob
import sys

logging.basicConfig(filename='app.log',level=logging.DEBUG)


initial_run = True


def _move_all_files_to_uploads(image_folder_path, dest_path):
    logging.info(f"Moving all files from {image_folder_path} to {dest_path}")
    print(f"Moving all files from {image_folder_path} to {dest_path}")
    if image_folder_path[-1] != '/':
        image_folder_path = image_folder_path + '/'

    image_files = [
        file
        for file in glob.glob(image_folder_path + '**', recursive=True)
        if file.endswith(".png") or file.endswith(".jpg")
    ]
    images_copy = []
    for image_file in image_files:
        image = os.path.basename(image_file)
        dest_file = os.path.join(dest_path, image)
        if not os.path.exists(dest_file):
            shutil.copyfile(os.path.join(image_file), dest_file)
        images_copy.append(dest_file)
    return images_copy


if __name__ == "__main__":
    """
    By default this will process only images in the uploads folder.
    Loading images that I have downloaded from the internet to make it easier to test.
    """
    script_args = sys.argv
    if (len(script_args)) < 2:
        help_stmt = "Please provide the path to the images folder eg: python reindex.py static/uploads"
        print(help_stmt)
        logging.info(help_stmt)
    elif (len(script_args)) > 2:
        logging.info("Please specify folder, and images will be recursively found")
    else:
        logging.info(f"Processing images from {script_args}")
        os.makedirs(config.IMAGES_UPLOAD_PATH, exist_ok=True)
        folder_path = script_args[1]
        print(f"Processing images in {folder_path}")
        images = _move_all_files_to_uploads(folder_path, config.IMAGES_UPLOAD_PATH)
        logging.info(f"Found {len(images)} images")
        print(f"Found {len(images)} images")
        annoy_reindex.reindex_annoy_and_update_database(images)
        logging.info("Finished processing images")