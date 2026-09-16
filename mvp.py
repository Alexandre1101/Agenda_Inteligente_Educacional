#import whisper
from pydantic import BaseModel
from typing import Optional
from ollama import chat
#import json

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


r'''
#transformando áudio em texto
model = whisper.load_model("large")
result = model.transcribe(
    r"C:\Users\alext\VS code pasta\python\estudos\mvp\mp3\borix.mp3",
    language="pt",
    fp16=False
)
texto = result["text"]
print(texto)
'''
texto = '''Bom dia, turma. Hoje vamos continuar a matéria de matemática, 
falando sobre frações e como simplificar frações equivalentes.

Ah, pessoal, lembrando que teremos prova de matemática 
no dia 20 de outubro, cobrindo frações e números decimais.

O João ficou com dúvida sobre como simplificar frações quando 
o numerador e o denominador são números grandes, então vamos 
retomar isso na próxima aula com mais exemplos.

A Mariana também perguntou se frações negativas seguem a mesma 
regra de simplificação, e expliquei que sim, o processo é o mesmo.

Só um adendo: o Pedro foi advertido hoje porque ficou mexendo 
no celular durante a explicação da matéria, mesmo depois de eu 
pedir duas vezes pra guardar.
'''
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
            "content": prompt
        }
    ],
    format=Aula.model_json_schema()
)


print(resposta.message.content)

