import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_monitor_endpoint(client):
    response = client.get('/api/v2/monitor')
    assert response.status_code == 200
    assert response.json == {"status": "Running smoothly"} 

def test_invalid_endpoint(client):
    response = client.get('/api/v2/invalid-endpoint')
    assert response.status_code == 404  # Expecting a 404 Not Found status
    assert response.json == {"error": "Not Found"}  # Adjust based on your API's error response format