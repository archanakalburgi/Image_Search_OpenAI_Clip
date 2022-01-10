pyenv virtualenv 3.8.10 shop
pyenv activate shop
eval "$(pyenv init --path)"
pip install annoy
pip install ftfy regex tqdm
pip install git+https://github.com/openai/CLIP.git
pip install scikit-image



# boo - has to do this to get the lza working
 PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.8.10

# Plan
Store all the image feature in to annoy tree and save the file on to the disk. 
![wd](plan.svg)


# Doubts
- Not sure how well the image search is going to look like

# Limitations
- Batch based, annoy tree cannot be updated in real time.


# Idead about scaling
Annoy has limitations
Works batchbaed, we might wan to get to real time soon
- https://milvus.io/bootcamp 
