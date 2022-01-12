import torch
import clip
from PIL import Image
import os
import skimage
from annoy import AnnoyIndex
import time
import sqlite3

images_path  = os.path.join(os.path.dirname(__file__), 'downloaded_images/images/small/00/')
vector_len = 512
image_vectors = AnnoyIndex(vector_len, 'angular')  # Length of item vector that will be indexed

device = "cuda" if torch.cuda.is_available() else "cpu"
image_files = [
    filename
    for filename in os.listdir(images_path)
    if filename.endswith(".png") or filename.endswith(".jpg")
]
print(f"Processing {len(image_files)} images")



connection = sqlite3.connect('database.db')
cur = connection.cursor()

model, preprocess = clip.load("ViT-B/32")

image_mapping = {}

for idx, filename in enumerate(image_files):
    image_path = os.path.join(images_path, filename)
    image = preprocess(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
    image_vector = torch.tensor(image).to(device)
    with torch.no_grad():
        output = model.encode_image(image_vector).float()
        out_vec = output.tolist()[0]
        image_vectors.add_item(idx, out_vec)
        image_mapping[idx] = filename
        cur.execute("INSERT INTO images (id, title, image_path) VALUES (?, ?, ?)",
            (idx, filename, filename)
        )


image_vectors.build(300) # 10 trees
image_vectors.save('test.ann')
connection.commit()
connection.close()

print("Done, not sleeping for a while")
time.sleep(1)

print("Loading index")
u = AnnoyIndex(vector_len, 'angular')
u.load('test.ann') # super fast, will just mmap the file


text_to_search = ["chairs"]
text_tokens = clip.tokenize(["This is " + desc for desc in text_to_search])

with torch.no_grad():
    text_vec = model.encode_text(text_tokens).float()


idx = u.get_nns_by_vector(text_vec.tolist()[0], 15)
for id in idx:
    print(f"Found {image_mapping[id]}")

        