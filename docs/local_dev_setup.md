# Local Dev Setup
We will be using pyenv.

```bash
penv install 3.8.10
pyenv virtualenv 3.8.10 shop
pyenv activate shop
eval "$(pyenv init --path)"
pip install -r requirements.txt
python main_app.py 
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
