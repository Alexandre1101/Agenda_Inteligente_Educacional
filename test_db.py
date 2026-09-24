"""
Script de Teste Completo do Banco de Dados SQLite.
Testa a integração entre os schemas do projeto e as tabelas SQLite.

Como rodar:
    python test_db.py
"""

import sqlite3
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para garantir importações relativas
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

from data.database import (
    DB_PATH,
    get_connection,
    criar_tabelas,
    salvar_aula_extraida,
    consultar_resumo_aula,
)

# Tenta importar os schemas Pydantic do projeto
try:
    from models.schemas import Aula, Prova, Duvida, Advertencia
    TEM_PYDANTIC = True
except ImportError:
    TEM_PYDANTIC = False


def separador(titulo: str):
    print("\n" + "=" * 60)
    print(f"  {titulo}")
    print("=" * 60)


def teste_1_criar_e_validar_schema():
    separador("TESTE 1: Criação e Validação do Schema")
    print(f"Caminho do banco: {DB_PATH}")

    # Cria as tabelas
    criar_tabelas()

    conn = get_connection()
    cursor = conn.cursor()

    # Consulta as tabelas criadas no SQLite
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    tabelas_encontradas = [row[0] for row in cursor.fetchall()]
    conn.close()

    tabelas_esperadas = [
        "aluno",
        "aula",
        "entrada",
        "exercicio",
        "ocorrencia",
        "prova",
        "turma",
        "usuario",
    ]

    print(f"Tabelas encontradas ({len(tabelas_encontradas)}): {', '.join(tabelas_encontradas)}")

    for t in tabelas_esperadas:
        assert t in tabelas_encontradas, f"❌ Tabela esperada '{t}' não foi encontrada!"

    print("✅ TESTE 1 APROVADO: Todas as 8 tabelas foram criadas com sucesso!")


def teste_2_persistencia_com_dados_do_projeto():
    separador("TESTE 2: Persistência com Objeto do Projeto")

    texto_transcricao = (
        "Hoje tivemos aula de matemática sobre equações do primeiro grau. "
        "A aluna Ana Clara teve dúvida sobre mudança de sinal ao isolar a incógnita. "
        "O aluno Lucas também perguntou sobre resolução de frações com incógnitas. "
        "O aluno Pedro levou uma advertência por uso de celular sem permissão. "
        "Atenção para a prova bimestral marcada para a próxima semana."
    )

    if TEM_PYDANTIC:
        print("Usando schemas Pydantic oficiais do projeto (models.schemas)...")
        aula_mock = Aula(
            materia="Matemática",
            assunto="Equações do Primeiro Grau",
            provas=[
                Prova(data="2026-10-02", materia="Prova Bimestral de Equações")
            ],
            duvidas=[
                Duvida(aluno="Ana Clara", descricao="Dúvida em mudança de sinal"),
                Duvida(aluno="Lucas", descricao="Dúvida em frações com incógnita"),
            ],
            advertencias=[
                Advertencia(aluno="Pedro", motivo="Uso indevido de celular em aula")
            ]
        )
    else:
        print("Usando dicionário estruturado equivalente ao Pydantic...")
        aula_mock = {
            "materia": "Matemática",
            "assunto": "Equações do Primeiro Grau",
            "provas": [{"data": "2026-10-02", "materia": "Prova Bimestral de Equações"}],
            "duvidas": [
                {"aluno": "Ana Clara", "descricao": "Dúvida em mudança de sinal"},
                {"aluno": "Lucas", "descricao": "Dúvida em frações com incógnita"},
            ],
            "advertencias": [
                {"aluno": "Pedro", "motivo": "Uso indevido de celular em aula"}
            ]
        }

    # Salva no banco de dados usando a função do módulo data
    aula_id = salvar_aula_extraida(
        aula_data=aula_mock,
        conteudo_texto=texto_transcricao,
        caminho_arquivo="data/audio/aula_teste.wav",
        origem="audio",
        turma_nome="Turma 3º Ano B",
        professor_nome="Prof. Carlos Silva",
        professor_email="carlos.silva@escola.com",
        data_aula="2026-09-23"
    )

    print(f"✅ Aula salva com sucesso no banco! ID gerado: {aula_id}")
    return aula_id


def teste_3_consulta_resumo(aula_id: int):
    separador("TESTE 3: Consulta e Relacionamentos no Banco")

    resumo = consultar_resumo_aula(aula_id)
    assert resumo is not None, f"❌ Não foi possível encontrar a aula ID {aula_id}!"

    print(f"📚 Nome da Aula:   {resumo['nome_aula']}")
    print(f"📖 Matéria:        {resumo['materia']}")
    print(f"🎯 Assunto:        {resumo['assunto']}")
    print(f"📅 Data da Aula:   {resumo['data_aula']}")
    print(f"🏫 Turma:          {resumo['turma']}")
    print(f"👨‍🏫 Professor:      {resumo['professor']}")
    print(f"🎙️ Origem:         {resumo['origem']}")
    print(f"📝 Transcrição:    {resumo['transcricao'][:70]}...")

    print(f"\n📋 Provas Registradas ({len(resumo['provas'])}):")
    for p in resumo["provas"]:
        print(f"   - [Data: {p['data_prova']}] {p['conteudo_prova']}")

    print(f"\n⚠️ Ocorrências Registradas ({len(resumo['ocorrencias'])}):")
    for o in resumo["ocorrencias"]:
        tipo_icone = "❓" if o["tipo"] == "duvida" else "🚨"
        print(f"   - {tipo_icone} [{o['tipo'].upper()}] Aluno: {o['aluno']} -> {o['descricao']}")

    assert len(resumo["provas"]) >= 1, "❌ Prova não encontrada no resumo!"
    assert len(resumo["ocorrencias"]) >= 3, "❌ Ocorrências não foram salvas corretamente!"

    print("\n✅ TESTE 3 APROVADO: Dados consultados e relacionados com sucesso!")


def teste_4_integridade_chaves_estrangeiras():
    separador("TESTE 4: Teste de Integridade Referencial (Foreign Keys)")

    conn = get_connection()
    cursor = conn.cursor()

    # Tentativa proposital de inserir uma aula com turma_id inexistente (ex: 999999)
    # Com PRAGMA foreign_keys = ON, o SQLite DEVE rejeitar e lançar sqlite3.IntegrityError
    try:
        cursor.execute("""
            INSERT INTO aula (nome_aula, assunto_aula, data_aula, materia_aula, entrada_id, turma_id)
            VALUES ('Aula Fantasma', 'Assunto', '2026-09-23', 'Matéria', 1, 999999)
        """)
        conn.commit()
        print("❌ ERRO: Chave estrangeira falhou! O banco permitiu turma inexistente.")
        conn.close()
        sys.exit(1)
    except sqlite3.IntegrityError:
        print("🛡️ Integridade confirmada: SQLite bloqueou inserção com chave estrangeira inválida!")
        conn.rollback()
    finally:
        conn.close()

    print("✅ TESTE 4 APROVADO: PRAGMA foreign_keys = ON está protegendo o banco!")


def main():
    print("🚀 INICIANDO TESTES DO BANCO DE DADOS DA AGEDA INTELIGENTE...")
    teste_1_criar_e_validar_schema()
    aula_id = teste_2_persistencia_com_dados_do_projeto()
    teste_3_consulta_resumo(aula_id)
    teste_4_integridade_chaves_estrangeiras()

    separador("RESULTADO FINAL")
    print("🎉 SUCESSO TOTAL! O banco SQLite está 100% pronto e integrado com o projeto.")
    print("=" * 60)


if __name__ == "__main__":
    main()

