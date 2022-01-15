import pytest
import image_search_main


@pytest.fixture
def app():
    app = image_search_main.create_app()
    return app
