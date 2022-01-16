import src.annoy_reindex as reindex
from src import config
import os
from annoy import AnnoyIndex

def test_write_vectors_and_images_create_two_files(connection):
    images = ["test.jpg", "test2.jpg", "grabage"]
    vectors = [[1]*512, [2]*512, [3]*512]
    reindex._write_vectors_and_images(connection, vectors, images)
    assert os.path.exists(config.ANNOY_INDEX_PATH)
    assert os.path.exists(config.DATABASE_PATH)


def test_write_vectors_and_images_create_should_create_relevant_entry(connection):
    images = ["test.jpg", "test2.jpg", "grabage"]
    vectors = [[1]*512, [2]*512, [3]*512]
    reindex._write_vectors_and_images(connection, vectors, images)
    cursor = connection.execute("SELECT id, image_path FROM images")
    rows = []
    for r in cursor:
        rows.append(r)
    assert rows == [(0, 'test.jpg'), (1, 'test2.jpg'), (2, 'grabage')]
    assert len(rows) == 3


def test_write_vectors_and_images_create_should_create_annoy_index(connection):
    images = ["test.jpg", "test2.jpg", "grabage"]
    vectors = [[1]*512, [2]*512, [3]*512]
    reindex._write_vectors_and_images(connection, vectors, images)
    assert os.path.exists(config.ANNOY_INDEX_PATH)
    search_index = AnnoyIndex(config.VECTOR_SIZE, config.ANNOY_METRIC)
    search_index.load(config.ANNOY_INDEX_PATH)
    ids = search_index.get_nns_by_vector([1]*512, 10, include_distances=False)
    assert ids == [0, 1, 2]

def test_reindex(connection):
    reindex.reindex_annoy_and_update_database(["tests/test_files/test.jpg"])
    assert os.path.exists(config.ANNOY_INDEX_PATH)
    assert os.path.exists(config.DATABASE_PATH)
    
    
    