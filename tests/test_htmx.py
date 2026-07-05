def test_grid_partial(client):
    response = client.get("/grid")
    assert response.status_code == 200
    # Should be an HTML partial, not a full document
    assert "<!DOCTYPE" not in response.text
    assert "Test Landscape" in response.text


def test_grid_filtered_by_category(client):
    response = client.get("/grid", params={"category": "portrait"})
    assert response.status_code == 200
    assert "Test Portrait" in response.text
    assert "Test Landscape" not in response.text


def test_grid_all_shows_all(client):
    response = client.get("/grid", params={"category": "all"})
    assert response.status_code == 200
    assert "Test Landscape" in response.text
    assert "Test Portrait" in response.text


def test_photo_lightbox(client):
    response = client.get("/photo/test-landscape")
    assert response.status_code == 200
    assert "Test Landscape" in response.text
    assert "Test Location" in response.text
    assert "Test Camera" in response.text


def test_photo_not_found(client):
    response = client.get("/photo/nonexistent")
    assert response.status_code == 404
