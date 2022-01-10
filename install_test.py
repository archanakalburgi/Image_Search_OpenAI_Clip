import torch
import clip
from PIL import Image
import os
import skimage

image_files = [filename for filename in  os.listdir(skimage.data_dir) if filename.endswith('.png') or filename.endswith('.jpg')]
print(len(image_files))
