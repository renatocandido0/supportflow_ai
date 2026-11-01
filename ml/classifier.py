from functools import lru_cache
from pathlib import Path
import joblib

from ml.text_processing import preparar_texto


CAMINHO_MODELO = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "supportflow_classifier.joblib"
)


@lru_cache(maxsize=1)
def carregar_modelo():
    return joblib.load(CAMINHO_MODELO)


def classificar_ticket(title: str, description: str) -> str:
    texto = preparar_texto(title, description)

    if not texto:
        raise ValueError("Título e descrição não podem estar vazios")

    artefatos = carregar_modelo()

    vetorizador = artefatos["vetorizador"]
    modelo = artefatos["modelo"]

    texto_numerico = vetorizador.transform([texto])
    previsao = modelo.predict(texto_numerico)

    return str(previsao[0])
