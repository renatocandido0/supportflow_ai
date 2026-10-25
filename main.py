from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
import sqlite3
from contextlib import asynccontextmanager
from database import inicializar_banco


@asynccontextmanager
async def lifespan(app: FastAPI):
    inicializar_banco()
    yield

app = FastAPI(lifespan=lifespan)


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Literal["low", "medium", "high", "urgent"]


class TicketStatusUpdate(BaseModel):
    status: Literal["open", "in_progress", "resolved"]


def abrir_conexao():
    connection = sqlite3.connect("supportflow.db")
    cursor = connection.cursor()
    return connection, cursor


def formatar_ticket(registro):
    ticket = {
        "id": registro[0],
        "title": registro[1],
        "description": registro[2],
        "priority": registro[3],
        "status": registro[4]
    }
    return ticket


@app.get("/tickets")
def listar_tickets():
    connection, cursor = abrir_conexao()
    cursor.execute("SELECT * FROM tickets")
    registros = cursor.fetchall()
    connection.close()

    tickets_formatados = []

    for registro in registros:
        ticket = formatar_ticket(registro)
        tickets_formatados.append(ticket)
    return tickets_formatados


@app.post("/tickets", status_code=201)
def criar_ticket(novo_ticket: TicketCreate):
    connection, cursor = abrir_conexao()

    cursor.execute(
        "INSERT INTO tickets (title, description, priority, status) VALUES (?, ?, ?, ?)",
        (novo_ticket.title,
         novo_ticket.description,
         novo_ticket.priority,
         "open")
    )
    connection.commit()

    novo_id = cursor.lastrowid

    connection.close()

    ticket_completo = {
        "id": novo_id,
        "title": novo_ticket.title,
        "description": novo_ticket.description,
        "priority": novo_ticket.priority,
        "status": "open"
    }
    return ticket_completo


@app.get("/tickets/{id}")
def buscar_ticket(id: int):
    connection, cursor = abrir_conexao()
    cursor.execute("SELECT * FROM tickets WHERE id = ?",
                   (id,)
                   )
    registro = cursor.fetchone()
    connection.close()
    if registro is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket não encontrado")
    return formatar_ticket(registro)


@app.patch("/tickets/{id}")
def atualizar_status(id: int, novo_status: TicketStatusUpdate):
    connection, cursor = abrir_conexao()
    cursor.execute(
        "UPDATE tickets SET status = ? WHERE id = ?",
        (novo_status.status, id)
    )
    linhas_afetadas = cursor.rowcount
    if linhas_afetadas == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Ticket não encontrado")

    cursor.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (id,)
    )

    registro = cursor.fetchone()
    connection.commit()
    connection.close()
    return formatar_ticket(registro)


@app.delete("/tickets/{id}", status_code=204)
def excluir_ticket(id: int):
    connection, cursor = abrir_conexao()
    cursor.execute(
        "DELETE FROM tickets WHERE id = ?",
        (id,)
    )

    linhas_afetadas = cursor.rowcount
    if linhas_afetadas == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Ticket não encontrado")

    connection.commit()
    connection.close()
