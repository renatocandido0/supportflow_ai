from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

app = FastAPI()


tickets = []
proximo_id = 1


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: Literal["low", "medium", "high", "urgent"]


class TicketStatusUpdate(BaseModel):
    status: Literal["open", "in_progress", "resolved"]


@app.get("/tickets")
def listar_tickets():
    return tickets


@app.post("/tickets", status_code=201)
def criar_ticket(novo_ticket: TicketCreate):
    global proximo_id
    id_do_ticket = proximo_id

    ticket_completo = {
        "id": id_do_ticket,
        "title": novo_ticket.title,
        "description": novo_ticket.description,
        "priority": novo_ticket.priority,
        "status": "open"
    }
    tickets.append(ticket_completo)
    proximo_id += 1
    return ticket_completo


@app.get("/tickets/{id}")
def buscar_ticket(id: int):
    for ticket in tickets:
        if ticket["id"] == id:
            return ticket
    raise HTTPException(
        status_code=404,
        detail="Ticket não encontrado")


@app.patch("/tickets/{id}")
def atualizar_status(id: int, novo_status: TicketStatusUpdate):
    for ticket in tickets:
        if ticket["id"] == id:
            ticket["status"] = novo_status.status
            return ticket
    raise HTTPException(
        status_code=404,
        detail="Ticket não encontrado")
