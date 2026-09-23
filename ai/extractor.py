from ollama import chat
from config import MODEL, PROMPT
from models.schemas import Aula
from pydantic import ValidationError


def extractor(texto):

    prompt = PROMPT.format(texto=texto)

    schema = Aula.model_json_schema()

    resposta = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=schema
    )

    try:
        aula = Aula.model_validate_json(resposta.message.content)

        return aula

    except ValidationError as erro:
        print("Os dados retornados pela IA não seguem o schema:")
        print(erro)
        print("\nResposta da IA:")
        print(resposta.message.content)

        return None


