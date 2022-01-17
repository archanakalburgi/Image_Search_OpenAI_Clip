# Deployment

## Building Docker image on M1 and running on Heroku
The Docker image is built on the M1 machine and then pushed to Heroku fails with a exec error. 

The fix is described here: https://stackoverflow.com/questions/66982720/keep-running-into-the-same-deployment-error-exec-format-error-when-pushing-nod 

If image building fails - https://stackoverflow.com/questions/44533319/how-to-assign-more-memory-to-docker-container from https://github.com/pytorch/pytorch/issues/1022


## Heroku Deployment
```sh
docker buildx build --platform linux/amd64 -t image-search .
docker tag image-search registry.heroku.com/shrouded-citadel-51973/web
docker push registry.heroku.com/shrouded-citadel-51973/web
heroku container:release web -a image-search
```
Notes: Model needs atleast of 1GB of memory. and heroku free is very limited

## Digital Ocean - 
Can use my eduction credit to deploy project, and deploy 
```sh
docker buildx build --platform linux/amd64 -t image-search .
docker tag image-search registry.digitalocean.com/image-search/image-search
docker push registry.digitalocean.com/image-search/image-search
```
Website live at [Here](https://image-search-ntmld.ondigitalocean.app/)<- Update this link before submitting.

