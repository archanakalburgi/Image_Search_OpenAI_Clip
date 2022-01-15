import os
import pytest
from flask import url_for


def test_index_should_return_200(client):
    assert client.get(url_for("index")).status_code == 200


def test_upload_should_return_200_for_valid_extensions(client):
    resp = client.post(
        url_for("upload"),
        data={
            "file": (
                os.path.join(os.path.dirname(__file__), "test_files/test.jpg"),
                "test.jpg",
            )
        },
    )
    assert resp.status_code == 200


def test_should_return_redirect_if_not_image(client):
    resp = client.post(
        url_for("upload"),
        data={
            "file": (
                os.path.join(os.path.dirname(__file__), "test_files/invalid.json"),
                "invalid.json",
            )
        },
    )
    assert resp.status_code == 302

def test_should_return_redirect_if_image_is_too_big(client):
    resp = client.post(
        url_for("upload"),
        data={
            "file": (
                os.path.join(os.path.dirname(__file__), "test_files/big_image.jpg"),
                "big_image.jpg",
            )
        },
    )
    assert resp.status_code == 413


def test_images_can_searched_with_images(client):
    """
    Goal of this test is to make sure annoy sql and views are working together. 
    Annoy and sql will be tested  separately.
    """
    resp = client.post(
        url_for("search"),
        data={
            "file": (
                os.path.join(os.path.dirname(__file__), "test_files/test.jpg"),
                "test.jpg",
            )
        },
    )
    assert resp.status_code == 200