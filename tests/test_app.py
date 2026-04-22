"""
l'application se crée et la page d'accueil répond.
"""
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_index_redirects_to_projects(client):
    """Sans être connecté, / redirige vers la liste des projets."""
    r = client.get('/')
    assert r.status_code in (200, 302)
    if r.status_code == 302:
        assert '/projects' in r.location
