"""
Setup do banco de dados SQLite para o projeto Agenda Inteligente Educacional.

Este arquivo cuida só da criação e conexão com o banco.
A lógica de Whisper/LLM continua no mvp.py, que importa este módulo.
"""

import sqlite3
from pathlib import Path

# Caminho do banco, ancorado na pasta onde este arquivo está — não no
# diretório de onde o script foi executado. Isso evita o problema de
# caminho relativo quebrar dependendo de como você roda o script
# (mesmo raciocínio já usado para os arquivos de áudio).
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "agenda.db"


def get_connection():
    """
    Abre uma conexão com o banco e ativa PRAGMA foreign_keys.

    Importante: essa PRAGMA precisa ser ativada em TODA conexão aberta,
    não só uma vez na criação do banco — o SQLite não guarda essa
    configuração no arquivo, ela é por conexão.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def criar_tabelas():
    """
    Cria todas as tabelas do schema, se ainda não existirem.
    Seguro rodar múltiplas vezes (usa IF NOT EXISTS).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        professor_nome VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        senha_hash VARCHAR(255) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS turma (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_turma VARCHAR(255) NOT NULL
        -- Nota: turma não está vinculada a usuario; todo professor vê
        -- todas as turmas (limitação aceita no MVP para usuário único).
    );

    CREATE TABLE IF NOT EXISTS aluno (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_aluno VARCHAR(255) NOT NULL,
        turma_id INTEGER NOT NULL,
        criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (turma_id) REFERENCES turma(id)
    );

    CREATE TABLE IF NOT EXISTS entrada (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origem VARCHAR(10) NOT NULL CHECK (origem IN ('audio', 'texto')),
        caminho_arquivo VARCHAR(255),
        conteudo_texto TEXT NOT NULL,
        usuario_id INTEGER NOT NULL,
        criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    );

    CREATE TABLE IF NOT EXISTS aula (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_aula VARCHAR(255) NOT NULL,
        assunto_aula VARCHAR(255) NOT NULL,
        data_aula DATE NOT NULL,
        materia_aula VARCHAR(100) NOT NULL,
        observacoes_gerais TEXT,
        entrada_id INTEGER NOT NULL UNIQUE,
        turma_id INTEGER NOT NULL,
        criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (entrada_id) REFERENCES entrada(id),
        FOREIGN KEY (turma_id) REFERENCES turma(id)
    );

    CREATE TABLE IF NOT EXISTS prova (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_prova DATE NOT NULL,
        conteudo_prova TEXT NOT NULL,
        aula_id INTEGER NOT NULL,
        FOREIGN KEY (aula_id) REFERENCES aula(id)
    );

    CREATE TABLE IF NOT EXISTS exercicio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao_exercicio TEXT NOT NULL,
        data_entrega DATE,
        aula_id INTEGER NOT NULL,
        criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (aula_id) REFERENCES aula(id)
    );

    CREATE TABLE IF NOT EXISTS ocorrencia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo VARCHAR(20) NOT NULL CHECK (
            tipo IN ('duvida', 'dificuldade', 'advertencia', 'desempenho')
        ),
        aluno_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        aula_id INTEGER NOT NULL,
        FOREIGN KEY (aluno_id) REFERENCES aluno(id),
        FOREIGN KEY (aula_id) REFERENCES aula(id)
    );

    CREATE INDEX IF NOT EXISTS idx_ocorrencia_aluno_tipo
        ON ocorrencia(aluno_id, tipo);

    """)

    conn.commit()
    conn.close()
    print(f"Banco criado/verificado em: {DB_PATH}")


if __name__ == "__main__":
    criar_tabelas()