# Make user uploaded images searchable

```sh
reindex.py static/user/uploads/
```
**Current Limitations**:
Right the vector images are not selectively indexed. Every time a full repo needs to be indexed. 
This is not great for a production app with a lot of new images every day.
