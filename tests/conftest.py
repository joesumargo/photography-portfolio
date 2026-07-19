from pathlib import Path

import pytest
from starlette.testclient import TestClient

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"


@pytest.fixture
def test_photos_yaml() -> Path:
    """Absolute path to test photo metadata YAML file."""
    return TEST_DATA_DIR / "photos.yaml"


@pytest.fixture
def test_collections_yaml() -> Path:
    """Absolute path to test collection metadata YAML file."""
    return TEST_DATA_DIR / "collections.yaml"


@pytest.fixture
def app(test_photos_yaml: Path, test_collections_yaml: Path):
    """FastAPI app instance wired to test data, with lifespan triggered."""
    from app.main import create_app

    application = create_app(
        photos_data_path=test_photos_yaml,
        collections_data_path=test_collections_yaml,
    )
    return application


@pytest.fixture
def client(app):
    """Test client that triggers lifespan on entry."""
    with TestClient(app) as c:
        yield c
