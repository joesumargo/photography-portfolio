def test_homepage_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_homepage_shows_monograph_elements(client):
    """Front page should show real collection and TOC placeholders."""
    response = client.get("/")
    assert "Featured Works" in response.text
    assert "Collection II." in response.text
    assert "Collection VI." in response.text


def test_homepage_has_sticky_note(client):
    """Sticky note navigation should be present on the front page."""
    response = client.get("/")
    assert "I." in response.text
    assert "VI." in response.text


def test_collection_page_returns_200(client):
    """GET /{collection_slug} returns the collection page."""
    response = client.get("/featured")
    assert response.status_code == 200
    assert "Featured Works" in response.text
    assert "text/html" in response.headers["content-type"]


def test_collection_not_found(client):
    """GET /nonexistent returns 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_collection_page_has_lightbox_triggers(client):
    """Collection page images should have HTMX lightbox attributes."""
    response = client.get("/featured")
    assert 'hx-get="/photo/test-landscape?src=' in response.text
    assert 'hx-target="#lightbox"' in response.text
