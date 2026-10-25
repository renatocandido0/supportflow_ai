from main import formatar_ticket


def test_formatar_ticket():
    registro = (
        1,
        "Erro no login",
        "Falha ao entrar",
        "high",
        "open"
    )

    resultado = formatar_ticket(registro)

    ticket = {
        "id": 1,
        "title": "Erro no login",
        "description": "Falha ao entrar",
        "priority": "high",
        "status": "open"
    }

    assert resultado == ticket
