import os
import torch
import clip
from PIL import Image
from annoy import AnnoyIndex
import shutil
import src.config as config
import sqlite3


import logging

# logging.basicConfig(filename='reindex.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)



def _generate_vector_from_image(images, clip_model, model_preprocess):
    vectors = []
    for image_file in images:
        # image_path = os.path.join(config.IMAGES_UPLOAD_PATH, image)
        image = (
            model_preprocess(Image.open(image_file).convert("RGB"))
            .unsqueeze(0)
            .to("cpu")
        )
        image_vector = torch.tensor(image).to("cpu")
        with torch.no_grad():
            output = clip_model.encode_image(image_vector).float()
            out_vec = output.tolist()[0]
            vectors.append(out_vec)
    return vectors


def _write_vectors_and_images(conn, vectors, images):
    """
    Write vectors and images paths to database along with Index
    Index needs to be constent across annoy index and the database, that is how we are doing to refer to it later.

    """
    annoy_index = AnnoyIndex(config.VECTOR_SIZE, "angular")
    for idx, (vector, image) in enumerate(zip(vectors, images)):
        annoy_index.add_item(idx, vector)
        conn.execute("INSERT OR REPLACE INTO images (id, title, image_path) VALUES (?, ?, ?)",
            (idx, image, image),
        )
    conn.commit()
    logging.info(
        f"Writing {len(vectors)} vectors to annoy index at {config.ANNOY_INDEX_PATH}"
    )
    annoy_index.build(300)
    annoy_index.save(config.ANNOY_INDEX_PATH)
    return



"""
Maybe right a thing to check for preconditons
1. Database that exits
2. Just create the uploads dir
3. Delete ann file 
"""
def reindex_annoy_and_update_database(images):
    os.makedirs(config.IMAGES_UPLOAD_PATH, exist_ok=True)
    conn = sqlite3.connect(config.DATABASE_PATH)
    # images = _get_images_from_folder_to_staged(images_path, config.IMAGES_UPLOAD_PATH)
    print("got so many", len(images))
    model, preprocess = clip.load("ViT-B/32", download_root=config.MODEL_DOWNLOAD_PATH)
    vectors = _generate_vector_from_image(images, model, preprocess)
    _write_vectors_and_images(conn, vectors, images)
    conn.close()
