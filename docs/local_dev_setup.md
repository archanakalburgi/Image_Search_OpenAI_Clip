# Local Dev Setup
To run the app on your computer aas quickly as possible.

Python dev env is 
Setup Python and [pyenv](https://github.com/pyenv/pyenv)  and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).
```bash
pyenv install 3.8.10
pyenv virtualenv 3.8.10 shop
eval "$(pyenv init --path)"
pyenv activate shop
```

```
pip install -r requirements.txt
python clean_dev.py
python reindex.py static/user/uploads
python main_app.py 
```


# Testing
```bash
pip install -r requirements_dev.txt
pytest tests
```

# Test Coverage
```bash
pytest --cov=src --cov-report=html
```
Here is the sample report:
```
---------- coverage: platform darwin, python 3.8.10-final-0 ----------
Name                   Stmts   Miss  Cover
------------------------------------------
src/__init__.py            0      0   100%
src/annoy_reindex.py      39      0   100%
src/annoy_search.py       34      0   100%
src/config.py             12      0   100%
src/db_util.py            27      0   100%
------------------------------------------
TOTAL                    112      0   100%

======================================================= 10 passed, 4 warnings in 2.72s ========================================================
(anno-ver) ➜  shopify-dev-intern git:(main) ✗
```

# Running project via docker
```
2. Run via docker
docker build -t image-search:latest .
docker run  -p 5550:5550 image-search
```

# FAQ

## Why does it run on Port 5050
On Mac 5000 is used by control center. So using 5050.

## Lza - Not Found error
This is rare, but ran into this because my python installation got to a bad state not sure how. Fixed by  
```bash
PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.8.10
```


## OSError 
This is because of how annoy index is created it is platform dependent. Fix this by removing the cashe/index.ann. 
Note: `clean_dev.py` actually does this. Follow the steps below.
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

## Why does reindex.py take so long
This is very noticable if we not using a GPU. Generating embeddings is a CPU bound task and takes longer. In a production environment we would use a GPU. 
and move it to a Data Pipeline and schedule it via Airflow.

## Why does it take 3-4 min to start up a web server?
If the application is running for the first time it will have to download the model. And the model is cached for the subsequent runs.
I probably could package that up. The down side is it is ~300MB.

## Can I just download docker image and run it?
Yes. heere is the image. 
```sh
docker pull ghcr.io/archanakalburgi/image-search:latest
docker run  -p 5550:5550 image-search
```

## Why is the repo so big?
Partly because I have checked in images as the other alternatives complicated code and setup.
