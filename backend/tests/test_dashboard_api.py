from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_dashboard_state_returns_initialized_payload():
    response = client.get('/dashboard/state')
    assert response.status_code == 200
    data = response.json()
    assert 'nodes' in data
    assert 'evacuation' in data
    assert data['nodes']


def test_flashover_simulation_updates_dashboard_state():
    response = client.post('/simulation/flashover/R2')
    assert response.status_code == 200
    payload = response.json()
    assert payload['scenario'] == 'FLASHOVER'
    state_response = client.get('/dashboard/state')
    state = state_response.json()
    assert state['nodes']['R2']['hazard_score'] >= 80
