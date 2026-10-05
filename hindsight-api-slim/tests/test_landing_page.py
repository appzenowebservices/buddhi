"""The API root serves a human-readable status page, not a JSON 404.

A browser hitting the API origin is usually a person checking the server is up;
these tests pin the page's contract — HTML, the brand mark, live status hooks,
the deployment's providers, and links that honor the configured base path.
"""

import os
from unittest.mock import MagicMock

from fastapi.testclient import TestClient


def _client() -> TestClient:
    from hindsight_api.api.http import create_app

    return TestClient(create_app(MagicMock(), initialize_memory=False))


def test_root_serves_html_landing_page():
    response = _client().get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    body = response.text
    assert "Welcome to your brain" in body
    assert "Hindsight" in body
    assert 'src="/logo.png"' in body
    assert 'id="api-dot"' in body
    assert 'id="db-dot"' in body
    assert "/health" in body
    assert "\033" not in body


def test_logo_asset_is_served_by_the_api():
    response = _client().get("/logo.png")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content.startswith(b"\x89PNG\r\n\x1a\n")


def test_root_is_not_part_of_the_api_surface():
    spec = _client().app.openapi()

    assert "/" not in spec["paths"]
    assert "/logo.png" not in spec["paths"]


def test_landing_page_links_follow_the_base_path():
    from hindsight_api.api.http import create_app
    from hindsight_api.config import clear_config_cache

    os.environ["HINDSIGHT_API_BASE_PATH"] = "/hindsight"
    clear_config_cache()
    try:
        response = TestClient(create_app(MagicMock(), initialize_memory=False)).get("/")
    finally:
        os.environ.pop("HINDSIGHT_API_BASE_PATH", None)
        clear_config_cache()

    assert response.status_code == 200
    assert 'const BASE = "/hindsight"' in response.text
    assert 'src="/hindsight/logo.png"' in response.text
    assert 'href="/hindsight/docs"' in response.text
    assert 'href="/hindsight/health"' in response.text
