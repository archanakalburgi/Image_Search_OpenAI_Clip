import pytest
import main_app


@pytest.fixture
def app():
    app = main_app.create_app()
    return app
