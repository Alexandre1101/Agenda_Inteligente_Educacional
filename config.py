# Arquivo para centralizar configurações do programa

MODEL = "llama3.2"

PROMPT = """
Analise a transcrição de uma aula.

Extraia somente informações que realmente aparecem no texto.
Não invente informações.

Categorias:

- materia: matéria estudada.
- assunto: assunto principal da aula.
- provas: avaliações ou provas mencionadas. Cada item deve ser um objeto com:
  - data: data ou momento mencionado para a prova.
  - materia: matéria da prova, se estiver disponível.
- duvidas: dúvidas dos alunos. Cada item deve ser um objeto com:
  - aluno: nome do aluno, se estiver disponível.
  - descricao: descrição da dúvida.
- advertencias: advertências mencionadas. Cada item deve ser um objeto com:
  - aluno: nome do aluno, se estiver disponível.
  - motivo: motivo da advertência.

Se uma informação não estiver presente, use null.

Retorne SOMENTE um JSON válido, exatamente nesta estrutura:

{{
    "materia": null,
    "assunto": null,
    "provas": [
        {{
            "data": null,
            "materia": null
        }}
    ],
    "duvidas": [
        {{
            "aluno": null,
            "descricao": null
        }}
    ],
    "advertencias": [
        {{
            "aluno": null,
            "motivo": null
        }}
    ]
}}

Se não houver provas, dúvidas ou advertências, use uma lista vazia.

Transcrição:

{texto}
"""

