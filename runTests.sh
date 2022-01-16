!/bin/bash


rm -rf .pytest_cache
pip install -r requirements_dev.txt
python reindex.py static/uploads/
pytest --cov=src tests/
