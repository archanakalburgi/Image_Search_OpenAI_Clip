# Vector Searching
- [Annoy](https://github.com/spotify/annoy)
    - Annoying part is, it is based on a file. 
    - And that file needs to be shipped around and vectors cannot be added on fly. Which is good and bad.
    - I have used this before, it is simple to use no complicated setup.
- [Faiss](https://github.com/facebookresearch/faiss)
    - Looks like the vectors can be added on fly.
    - Might not be great 
- [Hnsw](https://github.com/nmslib/hnswlib)
    - Very similar to annoy, with added bonus of being able to add vectors on fly.
    - This might be a good fit for what goals I have with this project.  
    - Wish to get a prototype of this.
- [Scann](https://github.com/google-research/google-research/tree/master/scann)
    - Readme says it supports linux primarily.
    - I have a mac and did not investigate this


# Vector Searching - Annoy
Sticking with annoy because it is simple and I have used in past. Will Speed up implementation.
Limitations:
- Cannot add vectors on fly. Will need to be generated offline and then update the API to use the file.


# Implementing a Web App instead of a REST API
API is an ideal choice for this project. Given that it is search and having something that has immediate visual feedback is a good for validation.  


# Deploying
This is good size application with different moving parts. Delploying to Heroku is something I have not done before this would be a great learning experience.


# Decision to upload 25k images to Github.
This is an odd decision that I made. The primary reason was to get something working on dev machine as quickly as possible without a lot of setup instructions. 
In a real world application we would store images in GCS and have CDN serve the images.


## Security
Security in this application is with respect to image size, file name and image type. The flask framework provides ways to setup authentication and authorization but for this project I have not used it. In future if the need be it can be added.