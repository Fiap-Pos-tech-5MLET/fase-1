from fastapi.testclient import TestClient
from app.main import app
from http import HTTPStatus

def test_root_deve_retornar_ok_e_status_code_200():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Ok"}


def test_rota_producao_sem_ano_status_ok_e_suceesso():
    client = TestClient(app)

    response = client.get('/api/producao')

    json_response = response.json()

    print(json_response)

    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"

def test_rota_producao_por_ano_status_ok_e_suceesso():
    client = TestClient(app)

    response = client.get('/api/producao/2015')

    json_response = response.json()

    print(json_response)

    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"

def test_rota_comercializacao_sem_ano_status_ok_e_suceesso():
    client = TestClient(app)

    response = client.get('/api/comercializacao')

    json_response = response.json()

    print(json_response)

    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"

def test_rota_comercializacao_por_ano_status_ok_e_suceesso():
    client = TestClient(app)

    response = client.get('/api/comercializacao/2014')

    json_response = response.json()

    print(json_response)

    assert response.status_code == HTTPStatus.OK
    assert json_response['status'] == "success"