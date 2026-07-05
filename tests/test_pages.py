def test_homepage_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_homepage_shows_monograph_elements(client):
    """Front page should show the location line and TOC placeholders."""
    response = client.get("/")
    assert "Based in the United Kingdom" in response.text
    assert "Collection One" in response.text
    assert "Collection Two" in response.text
    assert "Collection Six" in response.text


def test_homepage_has_sticky_note(client):
    """Sticky note navigation should be present on the front page."""
    response = client.get("/")
    assert "I." in response.text
    assert "VI." in response.text
