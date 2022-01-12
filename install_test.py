import torch
import clip
from PIL import Image
import os
from annoy import AnnoyIndex
import sqlite3
import src.config as config
from datetime import datetime

import logging
# logging.basicConfig(filename='data_pipeline.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
import shutil


"""
inputs - path_image_folder, path_annoy_index, path_database
"""


def _get_database_connection(database_path):
    conn = sqlite3.connect(database_path)
    return conn


def _create_database(conn, schema_file_path):
    logging.info("Creating database")
    with open(schema_file_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    logging.info("Database created")
def _get_images_from_folder(image_folder_path):
    image_files = [
        filename
        for filename in os.listdir(image_folder_path)
        if filename.endswith(".png") or filename.endswith(".jpg")
    ]
    logging.info(f"{len(image_files)} images found in {image_folder_path}")
    return image_files


images_path = os.path.join(
    os.path.dirname(__file__), "downloaded_images/images/small/00/"
)


def _generate_vector_from_image(images, clip_model, model_preprocess):
    for image in images:
        image_path = os.path.join(images_path, filename) # move this to _get_images_from_folder
        image = model_preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to("cpu")
        image_vector = torch.tensor(image).to("cpu")
        vectors = []
        with torch.no_grad():
            output = clip_model.encode_image(image_vector).float()
            out_vec = output.tolist()[0]
            vectors.append(out_vec)
    return vectors


def _write_vectors_and_images(conn, vectors, images, annoy_index_path):
    """
    Write vectors and images paths to database along with Index
    Index needs to be constext across annoy index and the database, that is how we are doing to refer to it later.

    """
    annoy_index = AnnoyIndex(config.VECTOR_SIZE, "angular")
    for idx, (vector, image) in enumerate(zip(vectors, images)):
        annoy_index.add_item(idx, vector)
        conn.execute(
            "INSERT INTO images (id, title, image_path) VALUES (?, ?, ?)",
            (idx, image, image),
        )
    conn.commit()
    logging.info(f"Writing {len(vectors)} vectors to annoy index at {config.INDEX_PATH}")
    annoy_index.build(300)
    annoy_index.save(config.INDEX_PATH)
    return
    

def _date_suffix(): #TODO test this
    back_folder_date = datetime.now().strftime("%Y_%m_%d")
    back_folder_hour = datetime.now().strftime("%M") # TODO: change this to %H after testing
    return back_folder_date + "/" + back_folder_hour

def _backup_path(asset): #TODO test this
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
            shutil.move(file_or_dir, backup_path) #If the samefile exists, it will be overwritten.?
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
    conn = _get_database_connection(config.DATABASE_PATH)
    _create_database(conn, config.SQL_SCRIPT_PATH)
    # images = _get_images_from_folder(images_path)

    # model, preprocess = clip.load("ViT-B/32")
    # vectors = _generate_vector_from_image(images, model, preprocess)
    # _write_vectors_and_images(conn, vectors, images, config.INDEX_PATH)
    # conn.close()
    # return


if __name__ == "__main__":
    main()