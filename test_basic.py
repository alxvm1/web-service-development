from app import app

def test_homepage():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b'Image Upload' in response.data

def test_process_missing_file():
    with app.test_client() as client:
        response = client.post('/process', data={'cell_size': 10})
        assert response.status_code == 400 or response.status_code == 500

