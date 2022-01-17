import glob
import os 
import shutil


image_folder_path = "static/uploads/"

image_files = [
    file
    for file in list(glob.iglob(image_folder_path + "**", recursive=True))
    if file.endswith(".png") or file.endswith(".jpg")
]

count = 0

for image_file in image_files:
    if count < 2000:
        count = count + 1
    else:
        os.remove(image_file)
