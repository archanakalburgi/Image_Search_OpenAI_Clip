# Local Dev Setup
We will be using pyenv.

```bash
pyenv virtualenv 3.8.10 shop
pyenv activate shop
eval "$(pyenv init --path)"
pip install -r requirements.txt
python app.py 
```

# PORT 
on Mac 5000 is used by control center. So using a different port.

# Running project
1. Create database with schema from scripts folder
```
python3 install.py
python3 reindex.py
```
2. Run via docker
docker run  -p 5550:5550 image-search

# Troubleshooting
## Lza - Not Found error
Fixed by  PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.8.10


## OSError 
```sh
Index size is not a multiple of vector size. Ensure you are opening using the same metric you used to create the index.: Undefined error: 0 (0)
Traceback (most recent call last):
  File "main_app.py", line 4, in <module>
    import src.annoy_search as ann
  File "/Users/archanakalburgi/shopify_coding_challenge/shopify-dev-intern/src/annoy_search.py", line 14, in <module>
    search_index.load(config.ANNOY_INDEX_PATH)
OSError: Index size is not a multiple of vector size. Ensure you are opening using the same metric you used to create the index.: Undefined error: 0 (0)
```
Fixed by running following commands
```sh
python clean_dev.py
python reindex.py static/uploads/
```