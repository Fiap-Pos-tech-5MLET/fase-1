from fastapi.testclient import TestClient
from app.main import app
from http import HTTPStatus
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME_TEST = os.getenv('USERNAME_TEST')
PASSWORD_TEST = os.getenv('PASSWORD_TEST')

def get_token(client):
    # Efetua a autenticacao para pegar o token e validar a chamada passando token
    response_auth = client.post('/api/login', json={'username': USERNAME_TEST, 'password': PASSWORD_TEST})

    assert response_auth.status_code == HTTPStatus.OK
    return response_auth.json()['access_token']

def test_root_deve_retornar_ok_e_status_code_200():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    # assert response.json() == {"message": "Ok"}

def test_rota_producao_por_ano_status_ok_e_sucesso():
    client = TestClient(app)

    token = get_token(client)

    response = client.get('/api/producao/2015', headers={'Authorization': f'Bearer {token}'})
    json_response = response.json()
    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"

def test_rota_comercializacao_por_ano_status_ok_e_sucesso():
    client = TestClient(app)

    token = get_token(client)

    response = client.get('/api/comercializacao/2014', headers={'Authorization': f'Bearer {token}'})

    json_response = response.json()

    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"

def test_rota_exportacao_por_ano_status_ok_e_sucesso():
    client = TestClient(app)

    token = get_token(client)

    response = client.get('/api/exportacao/2014/vinhos_de_mesa', headers={'Authorization': f'Bearer {token}'})

    json_response = response.json()

    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"

def test_rota_importacao_por_ano_status_ok_e_sucesso():
    client = TestClient(app)

    token = get_token(client)

    response = client.get('/api/importacao/2023/espumantes', headers={'Authorization': f'Bearer {token}'})

    json_response = response.json()

    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"

def test_rota_processamento_por_ano_status_ok_e_sucesso():
    client = TestClient(app)

    token = get_token(client)

    response = client.get('/api/processamento/2023/viniferas', headers={'Authorization': f'Bearer {token}'})

    json_response = response.json()

    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"