# Semantic Search Using Clip
Assumption: we have images and text describing the images. (eg. in a Shopify store where a user is searching for a product from text or image)

Clip is interesting because it is designed to learn about the image, not just by using **image features** but also the **text** description describing the image. Specifics of the model and its limitations discussed in the [blog](https://openai.com/blog/clip/). 

In this project we are generating embeddings for images that we assume are in the image repository. Which is designed to work in a batch fashion. Generated embeddings are stored in an Annoy tree. Using the annoy tree we can search for images based on the embedding. Using Annoy's API and file-based nature makes storing, distributing and retrieving embeddings simple. 

## Limitations
- Annoy's file based nature is not suitable for large amounts of data.
- Building the Annoy Index is batch based, that means we will have to restart the application every time we rebuild the index or have a complicated deployment to handle the downtime.
- It is very tricky to determine when the image search is not yielding any relevant results. And it might be difficult to automate this test. 
For the purposes of this project we are using the images data set from [ABO Dataset](https://amazon-berkeley-objects.s3.amazonaws.com/index.html).


# References
- [OpenAI](https://openai.com/blog/clip/)
