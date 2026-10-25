import sqlite3


def inicializar_banco():
    connection = sqlite3.connect("supportflow.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL);
    """)
    connection.commit()
    connection.close()
