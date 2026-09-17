#arquivo para centralizar funçoes da extração de dados do texto transcrito, podemos deixar o prompt aqui ou em config
from ollama import chat
from config import MODEL, PROMPT
from models.schemas import Aula
import json
from pydantic import ValidationError


def extractor(texto):
    prompt = PROMPT.format(texto=texto)

    resposta = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    try:
        dados = json.loads(resposta.message.content)
        aula = Aula.model_validate(dados)

        return aula

    except json.JSONDecodeError:
        print("A IA não retornou um JSON válido.")
        return None

    except ValidationError as erro:
        print("Os dados retornados pela IA não seguem o schema:")
        print(erro)
        return None
