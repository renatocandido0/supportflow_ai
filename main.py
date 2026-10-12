from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


tickets = []
proximo_id = 1


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str


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
