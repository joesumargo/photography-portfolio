def test_homepage_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Test Landscape" in response.text
    assert "Test Portrait" in response.text


def test_homepage_contains_categories(client):
    response = client.get("/")
    assert "landscape" in response.text.lower()
    assert "portrait" in response.text.lower()


def test_homepage_has_htmx_attributes(client):
    response = client.get("/")
    assert "hx-get" in response.text
    assert "hx-target" in response.text
