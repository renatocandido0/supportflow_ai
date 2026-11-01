import pytest
from fastapi.testclient import TestClient
import main


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "inicializar_banco", lambda: None)

    with TestClient(main.app) as cliente:
        yield cliente


def test_classificacao_sucesso(client, monkeypatch):
    monkeypatch.setattr(
        main,
        "classificar_ticket",
        lambda title, description: "access"
    )

    resposta = client.post(
        "/tickets/classify",
        json={
            "title": "Problema no login",
            "description": "Minha senha não funciona"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        "predicted_category": "access"
    }


def test_classificacao_texto_vazio(client, monkeypatch):
    def classificador_simulado(title, description):
        raise ValueError("Título e descrição não podem estar vazios")

    monkeypatch.setattr(
        main,
        "classificar_ticket",
        classificador_simulado
    )

    resposta = client.post(
        "/tickets/classify",
        json={
            "title": "",
            "description": ""
        }
    )

    assert resposta.status_code == 422


def test_classificacao_campo_obrigatorio(client):
    resposta = client.post(
        "/tickets/classify",
        json={
            "title": "Problema de acesso"
        }
    )

    assert resposta.status_code == 422


def test_classificacao_modelo_real(client):
    resposta = client.post(
        "/tickets/classify",
        json={
            "title": "Não consigo acessar minha conta",
            "description": "Minha senha não funciona"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        "predicted_category": "access"
    }
