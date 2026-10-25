import sqlite3
import pytest
import main

from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    banco_teste = tmp_path / "teste.db"

    connection = sqlite3.connect(banco_teste)
    connection.execute("""
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

    def abrir_conexao_teste():
        connection = sqlite3.connect(banco_teste)
        return connection, connection.cursor()

    monkeypatch.setattr(
        main, "abrir_conexao", abrir_conexao_teste
    )

    def evitar_inicializacao_real():
        pass

    monkeypatch.setattr(
        main, "inicializar_banco", evitar_inicializacao_real
    )

    with TestClient(main.app) as test_client:
        yield test_client


def test_criar_ticket(client):
    resposta = client.post("/tickets", json={
        "title": "Erro no login",
        "description": "Falha ao acessar",
        "priority": "high"
    })

    assert resposta.status_code == 201
    assert resposta.json()["id"] == 1
    assert resposta.json()["status"] == "open"


def test_listar_e_buscar_tickets(client):
    client.post("/tickets", json={
        "title": "Erro no pagamento",
        "description": "Pagamento recusado",
        "priority": "medium"
    })

    resposta = client.get("/tickets")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1

    resposta = client.get("/tickets/1")
    assert resposta.status_code == 200
    assert resposta.json()["title"] == "Erro no pagamento"


def test_atualizar_status(client):
    client.post("/tickets", json={
        "title": "Teste PATCH",
        "description": "Verificar atualização",
        "priority": "low"
    })

    resposta = client.patch(
        "/tickets/1",
        json={"status": "resolved"}
    )

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "resolved"

    consulta = client.get("/tickets/1")
    assert consulta.json()["status"] == "resolved"


def test_excluir_ticket(client):
    client.post("/tickets", json={
        "title": "Teste DELETE",
        "description": "Verificar exclusão",
        "priority": "low"
    })

    resposta = client.delete("/tickets/1")
    assert resposta.status_code == 204

    consulta = client.get("/tickets/1")
    assert consulta.status_code == 404


def test_erros_404(client):
    assert client.get("/tickets/999").status_code == 404

    assert client.patch(
        "/tickets/999",
        json={"status": "resolved"}
    ).status_code == 404

    assert client.delete("/tickets/999").status_code == 404


def test_validacoes_422(client):
    resposta = client.post("/tickets", json={
        "title": "Teste inválido",
        "description": "Prioridade inexistente",
        "priority": "extreme"
    })

    assert resposta.status_code == 422

    resposta = client.patch(
        "/tickets/1",
        json={"status": "invalid"}
    )

    assert resposta.status_code == 422
