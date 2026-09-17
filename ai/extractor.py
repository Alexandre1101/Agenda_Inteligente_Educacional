#arquivo para centralizar funçoes da extração de dados do texto transcrito, podemos deixar o prompt aqui ou em config
from ollama import chat
from config import MODEL, PROMPT


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

    return resposta.message.content