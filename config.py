# Arquivo para centralizar configurações do programa

MODEL = "llama3.2"

PROMPT = """
Analise a transcrição de uma aula.

Extraia somente informações que realmente aparecem no texto.

Categorias:

- materia: matéria estudada
- assunto: assunto da aula
- provas: avaliações mencionadas
- duvidas: dúvidas dos alunos
- advertencias: alunos advertidos

Não invente informações. Corrija erros de concordância verbal.
Se uma informação não estiver presente, deixe o campo vazio.

Retorne somente um JSON neste formato:

{{
    "materia": "",
    "assunto": "",
    "provas": [],
    "duvidas": [],
    "advertencias": []
}}

Transcrição:

{texto}
"""
