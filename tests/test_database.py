import sqlite3
import main

from fastapi.testclient import TestClient


def test_inicializacao_banco(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    banco = tmp_path / "supportflow.db"

    assert not banco.exists()

    with TestClient(main.app):
        pass

    assert banco.exists()

    connection = sqlite3.connect(banco)

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name = 'tickets'
        """)

        resultado = cursor.fetchone()

        assert resultado is not None
        assert resultado[0] == "tickets"

    finally:
        connection.close()
