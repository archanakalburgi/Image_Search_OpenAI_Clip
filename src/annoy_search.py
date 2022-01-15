import torch
import clip
from PIL import Image
from annoy import AnnoyIndex

from src import db_util

from . import config
import logging

device = "cuda" if torch.cuda.is_available() else "cpu"
search_index = AnnoyIndex(config.VECTOR_SIZE, config.ANNOY_METRIC)

search_index.load(config.ANNOY_INDEX_PATH)
model, preprocess = clip.load("ViT-B/32", download_root=config.MODEL_DOWNLOAD_PATH)


def text_search(search_term):
    logging.info(f"Searching for {search_term}")
    search_term_token = clip.tokenize(["This is " + desc for desc in [search_term]])
    with torch.no_grad():
        text_vec = model.encode_text(search_term_token).float()

    ids = search_index.get_nns_by_vector(
        text_vec.tolist()[0], config.NUM_OF_NEAREST_NEIGHBORS, include_distances=False
    )
    return ids


def image_search(search_image_path):
    logging.info(f"Searching for {search_image_path}")
    image_path = Image.open(search_image_path).convert("RGB")
    image = preprocess(image_path).unsqueeze(0).to(device)
    image_vector = torch.tensor(image).to(device)
    with torch.no_grad():
        image_vec = model.encode_image(image_vector).float()
    ids = search_index.get_nns_by_vector(
        image_vec.tolist()[0], config.NUM_OF_NEAREST_NEIGHBORS, include_distances=False
    )
    return ids


def search(search_type, search_term_or_image_path):
    """
    How to handle the when distance is too high? what is to high?
    """
    if search_type == "text":
        ids = text_search(search_term_or_image_path)
    elif search_type == "image":
        ids = image_search(search_term_or_image_path)
    else:
        ids = []
    # print(ids[1]) to make decision based on distace seems hard.
    return db_util.get_image_from_database(ids)
