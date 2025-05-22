from fastapi.testclient import TestClient
from app.main import app
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME_TEST = os.getenv('USERNAME_TEST')
PASSWORD_TEST = os.getenv('PASSWORD_TEST')

def test_autenticacao_status_ok_e_sucesso():
    client = TestClient(app)
    response_auth = client.post('/api/login', json={'username': USERNAME_TEST, 'password': PASSWORD_TEST})

    assert response_auth.status_code == HTTPStatus.OK
    assert response_auth.json()['access_token'] != None

