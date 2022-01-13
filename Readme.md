pyenv virtualenv 3.8.10 shop
pyenv activate shop
eval "$(pyenv init --path)"
pip install annoy
pip install ftfy regex tqdm
pip install git+https://github.com/openai/CLIP.git
pip install scikit-image




# Plan
Store all the image feature in to annoy tree and save the file on to the disk. 
![wd](plan.svg)


## Implementation Plan
### V1
- [x] Make sure the plan is doable MVP (in ipynb)
    - [x] Annoy tree store and retrive - done
    - [x] Image feature extraction - done
    - [x] Image search is it any good? - Good, as far as we have good amount of images indexed
- [x] Back End - (Using flask)
    - [x] API to search - Building a react app would be nice, but tome consuming. So using Flask Views
    - [x] API to upload image for search - Done
    - [X] API to add images to repo(may be) - 
            Images can be uploaded by the user to index. But index is batch based, would need be done by the user. In future we can add a airflow job to run every hour to keep the index updated. 
- [x] Front End - (Using boot strap)
    - [x] Grid of images limit to 16 images a page
    - [x] Search text box
    - [x] Search image box 
    - [ ] Make it look like, an adult made it. 
- [x] Deployment 
    - [x] local server setup instructions
    - [x] DockerFile so that it is easy to get the application running.
    - [x] Heroku deployment - deployed to digital ocean instead of heroku

### V2
- [ ] Automate index creation when new images are added to the repo.
- [ ] Use fast API to get, so that API can be used by other projects
- [ ] React App would be nice.


## Assumptions
- Do not send over a lager setup instructions over, it might no work.
- Should be able to run the project in 10 min. 
- Should be able feel what this project is about without having to get the whole thing running
    - Host it on heroku?
    - Make a docker image? so that it just runs (docker is everywhere?)

# Running project
1. Create database with schema from scripts folder
```
python3 scripts/create_db.py
```
2. Run via docker
docker run  -p 5550:5550 image-search
# Doubts
- Not sure how well the image search is going to look like

# Why annoy 

# Auth is tricy
# Limitations
- Batch based, annoy tree cannot be updated in real time.


# Idead about scaling
Annoy has limitations
Works batchbaed, we might wan to get to real time soon
- https://milvus.io/bootcamp 
