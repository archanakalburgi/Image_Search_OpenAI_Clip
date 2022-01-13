"""
Script is used to updated the existing database with new images.
scans the config.IMAGE_FOLDER_PATH and adds any new images that where uploads.


Assumptions:
The filename for the images is assumed to be unique.(The controller that handled uploaded might need to be updated to check for duplication.)
"""

import src.annoy_reindex as annoy_reindex
import os
import pathlib
import logging
import shutil
from src import config
import glob

# logging.basicConfig(filename='reindex.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

raw_images_path = "downloaded_images/images/small/"
images_path = os.path.join(os.path.dirname(__file__), raw_images_path)
path = pathlib.Path().resolve()


initial_run = True


def move_all_files_to_uploads(image_folder_path, dest_path):
    image_files = [
        file
        for file in list(glob.iglob(images_path + "**", recursive=True))
        if file.endswith(".png") or file.endswith(".jpg")
    ]
    images_copy = []
    logging.info(f"{len(image_files)} images found in {image_folder_path}")

    # May be move them to staged, and then read from staged. which might be annothing
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
    images = []
    os.makedirs(config.IMAGES_UPLOAD_PATH, exist_ok=True)
    if initial_run:
        source_path = path.joinpath(images_path)
        print(f"Loading from {source_path}")
        images = move_all_files_to_uploads(source_path, config.IMAGES_UPLOAD_PATH)
        print(len(images))
        annoy_reindex.reindex_annoy_and_update_database(images)
    else:
        print("handling just uploads")
