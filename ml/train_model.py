import csv
import joblib
from pathlib import Path
from text_processing import preparar_texto
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

textos = []
categorias = []

with open("data/tickets.csv", encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)
    for ticket in leitor:
        textos.append(preparar_texto(ticket['title'], ticket['description']))
        categorias.append(ticket['category'])


print("Total de textos:", len(textos))
print("Total de categorias:", len(categorias))
print("Primeiro texto:", textos[0])
print("Primeira categoria:", categorias[0])

vetorizador = TfidfVectorizer()
matriz_tfidf = vetorizador.fit_transform(textos)

print(matriz_tfidf.shape)

modelo = LogisticRegression()

modelo.fit(matriz_tfidf, categorias)

Path("models").mkdir(exist_ok=True)

joblib.dump(
    {
        "vetorizador": vetorizador,
        "modelo": modelo
    },
    "models/supportflow_classifier.joblib"
)

print("Modelo salvo com sucesso!")

print(modelo.classes_)

novos_tickets = [
    "Minha conta não aceita o login",
    "Minha cobrança veio com valor diferente",
    "O aplicativo congela quando tento enviar uma imagem",
    "Gostaria de sugerir melhorias na plataforma"
]

for ticket in novos_tickets:
    ticket_numerico = vetorizador.transform([ticket])
    categoria_prevista = modelo.predict(ticket_numerico)
    print(f"Ticket: {ticket}")
    print(f"Previsão: {categoria_prevista[0]}")


textos_teste = []
categorias_reais = []

with open("data/tickets_test.csv", encoding="utf-8", newline="") as arquivo:
    leitor = csv.DictReader(arquivo)
    for ticket in leitor:
        textos_teste.append(preparar_texto(
            ticket['title'], ticket['description']))
        categorias_reais.append(ticket['category'])

for ticket in textos_teste:
    ticket_numerico = vetorizador.transform([ticket])
    categoria_prevista = modelo.predict(ticket_numerico)
    print(f"Ticket: {ticket}")
    print(f"Previsão: {categoria_prevista[0]}")

matriz_teste = vetorizador.transform(textos_teste)
previsoes = modelo.predict(matriz_teste)

accuracy = accuracy_score(categorias_reais, previsoes)

print(f"Accuracy: {accuracy:.1%}")
