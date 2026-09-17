# Arquivo para centralizar configurações do programa

MODEL = "llama3.2"

PROMPT = """
Analise a transcrição de uma aula.

Extraia somente informações que realmente aparecem no texto.

Retorne exclusivamente um JSON válido, sem markdown e sem explicações.

O JSON deve seguir exatamente esta estrutura:

{
    "materia": null,
    "assunto": null,
    "provas": [],
    "duvidas": [],
    "advertencias": []
}

Cada prova deve seguir:
{
    "data": null,
    "materia": null
}

Cada dúvida deve seguir:
{
    "aluno": null,
    "descricao": ""
}

Cada advertência deve seguir:
{
    "aluno": null,
    "motivo": ""
}

Regras:

- Não invente informações.
- Se a matéria não aparecer, use null.
- Se o assunto não aparecer, use null.
- Se não houver provas, use [].
- Se não houver dúvidas, use [].
- Se não houver advertências, use [].
- Use somente informações presentes na transcrição.

Transcrição:

{texto}
"""
