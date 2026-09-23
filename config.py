# Arquivo para centralizar configurações do programa

MODEL = "llama3.2"

PROMPT = """
Analise a transcrição de uma aula.

Extraia somente informações que realmente aparecem no texto.

Não invente informações.

Identifique:
- matéria estudada
- assunto da aula
- provas ou avaliações mencionadas
- dúvidas dos alunos
- advertências

Quando uma informação não estiver presente, use null
quando o campo for opcional.

Quando não houver itens em provas, duvidas ou advertencias,
retorne uma lista vazia.

Retorne somente os dados solicitados no schema.

Transcrição:

{texto}
"""
