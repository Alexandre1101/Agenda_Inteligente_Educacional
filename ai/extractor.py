from ollama import chat
from config import MODEL, PROMPT
from models.schemas import Aula
from pydantic import ValidationError
import json


def extractor(texto):

    prompt = PROMPT.format(texto=texto)

    resposta = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    try:
        dados = json.loads(resposta.message.content)

        aula = Aula.model_validate(dados)

        return aula

    except json.JSONDecodeError as erro:
        print("A IA não retornou um JSON válido.")
        print(resposta.message.content)
        print(erro)
        return None

    except ValidationError as erro:
        print("Os dados retornados pela IA não seguem o schema:")
        print(erro)
        return None
