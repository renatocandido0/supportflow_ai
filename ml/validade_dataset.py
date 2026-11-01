import csv


categorias_validas = {
    "access",
    "billing",
    "technical_issue",
    "other"
}

erros = 0

with open("data/tickets.csv", encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)
    for numero_linha, ticket in enumerate(leitor, start=2):
        if ticket['category'] not in categorias_validas:
            print(
                f"Linha {numero_linha}: Categoria inválida: {ticket['category']}")
            print()
            erros += 1

        else:
            print(f"Titulo: {ticket['title']}")
            print(f"Categoria: {ticket['category']}")
            print()

if erros > 0:
    print(f"Total de erros encontrados: {erros}")
else:
    print("Nenhum erro encontrado")
