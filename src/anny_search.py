import torch
import clip
from PIL import Image
from annoy import AnnoyIndex

from . import config
# from . import db_util

device = "cuda" if torch.cuda.is_available() else "cpu"
search_index = AnnoyIndex(config.VECTOR_SIZE, 'angular')  # Length of item vector that will be indexed
search_index.load("src/test.ann") # this needs to be hot swappable, not sure how to do it.
model, preprocess = clip.load("ViT-B/32",download_root=config.MODEL_DOWNLOAD_PATH)

#db connect

def text_search(search_term):
    print("searching now")
    search_term_token = clip.tokenize(["This is " + desc for desc in [search_term]])
    with torch.no_grad():
        text_vec = model.encode_text(search_term_token).float()

    ids = search_index.get_nns_by_vector(text_vec.tolist()[0], 10)
    return ids

def image_search(search_image_path):
    print("searching now")
    image_path = Image.open(search_image_path).convert("RGB")
    image = preprocess(image_path).unsqueeze(0).to(device)
    image_vector = torch.tensor(image).to(device)
    with torch.no_grad():
        output = model.encode_image(image_vector).float()
        out_vec = output.tolist()[0]
    ids = search_index.get_nns_by_vector(out_vec, 10)
    return ids
# search image has to be different functions.