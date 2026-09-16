import whisper
from pydantic import BaseModel
from typing import Optional
from ollama import chat
import json

#Definindo como os dados serão salvos
class Prova(BaseModel):
    data: Optional[str] = None
    materia: Optional[str] = None


class Duvida(BaseModel):
    aluno: Optional[str] = None
    descricao: str


class Advertencia(BaseModel):
    aluno: Optional[str] = None
    motivo: str


class Aula(BaseModel):
    materia: Optional[str] = None
    assunto: Optional[str] = None
    provas: list[Prova] = []
    duvidas: list[Duvida] = []
    advertencias: list[Advertencia] = []

#transformando áudio em texto
model = whisper.load_model("large")
result = model.transcribe(
    r"C:\Users\alext\VS code pasta\python\estudos\mvp\borix.mp3",
    language="pt",
    fp16=False
)
texto = result["text"]
print(texto)
#passando texto para formatação com llm
prompt = f"""
Analise a transcrição de uma aula.

Extraia somente informações que realmente aparecem no texto.

Categorias:

- materia: matéria estudada
- assunto: assunto da aula
- provas: avaliações mencionadas
- duvidas: dúvidas dos alunos
- advertencias: alunos advertidos

Não invente informações.
Se uma informação não estiver presente, deixe o campo vazio.

Transcrição:

{texto}
"""
resposta = chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": f"{prompt}"
        }
    ]
)

print(resposta.message.content)


json_texto = resposta.message.content

dados_dict = json.loads(json_texto)

aula = Aula.model_validate(dados_dict)