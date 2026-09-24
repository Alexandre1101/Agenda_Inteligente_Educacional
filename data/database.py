"""
Setup do banco de dados SQLite para o projeto Agenda Inteligente Educacional.

Este arquivo cuida da criação, conexão e persistência de dados no banco.
A lógica de Whisper/LLM continua no mvp.py ou services, que importam este módulo.
"""

import sqlite3
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional

# Caminho do banco, ancorado na pasta onde este arquivo está — não no
# diretório de onde o script foi executado. Isso evita o problema de
# caminho relativo quebrar dependendo de como você roda o script
# (mesmo raciocínio já usado para os arquivos de áudio).
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "agenda.db"


def get_connection() -> sqlite3.Connection:
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


# ==============================================================================
# Funções Auxiliares de Persistência para o Projeto
# ==============================================================================

def obter_ou_criar_usuario(
    conn: sqlite3.Connection,
    professor_nome: str = "Professor Padrão",
    email: str = "professor@escola.com",
    senha_hash: str = "123456"
) -> int:
    """Busca um usuário pelo email ou cria um novo se não existir."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuario WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(
        "INSERT INTO usuario (professor_nome, email, senha_hash) VALUES (?, ?, ?)",
        (professor_nome, email, senha_hash)
    )
    return cursor.lastrowid


def obter_ou_criar_turma(conn: sqlite3.Connection, nome_turma: str = "Turma 1A") -> int:
    """Busca uma turma pelo nome ou cria uma nova se não existir."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM turma WHERE nome_turma = ?", (nome_turma,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("INSERT INTO turma (nome_turma) VALUES (?)", (nome_turma,))
    return cursor.lastrowid


def obter_ou_criar_aluno(conn: sqlite3.Connection, nome_aluno: str, turma_id: int) -> int:
    """Busca um aluno pelo nome na turma especificada ou cria um novo."""
    cursor = conn.cursor()
    nome_sanitizado = (nome_aluno or "Aluno Não Identificado").strip()
    cursor.execute(
        "SELECT id FROM aluno WHERE nome_aluno = ? AND turma_id = ?",
        (nome_sanitizado, turma_id)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute(
        "INSERT INTO aluno (nome_aluno, turma_id) VALUES (?, ?)",
        (nome_sanitizado, turma_id)
    )
    return cursor.lastrowid


def salvar_aula_extraida(
    aula_data: Any,
    conteudo_texto: str,
    caminho_arquivo: Optional[str] = None,
    origem: str = "audio",
    turma_nome: str = "Turma 1A",
    professor_nome: str = "Professor Padrão",
    professor_email: str = "professor@escola.com",
    data_aula: Optional[str] = None
) -> int:
    """
    Persiste os dados de uma aula extraída (instância de Aula Pydantic ou dict)
    no banco de dados SQLite dentro de uma transação.
    Retorna o ID da aula criada.
    """
    if data_aula is None:
        data_aula = date.today().isoformat()

    # Normalizar aula_data para dict compatível com Pydantic v1, v2 ou dict simples
    if hasattr(aula_data, "model_dump"):
        dados = aula_data.model_dump()
    elif isinstance(aula_data, dict):
        dados = aula_data
    elif hasattr(aula_data, "dict"):
        dados = aula_data.dict()
    else:
        dados = {
            "materia": getattr(aula_data, "materia", "Geral"),
            "assunto": getattr(aula_data, "assunto", "Não informado"),
            "provas": getattr(aula_data, "provas", []),
            "duvidas": getattr(aula_data, "duvidas", []),
            "advertencias": getattr(aula_data, "advertencias", [])
        }

    materia = dados.get("materia") or "Geral"
    assunto = dados.get("assunto") or "Conteúdo Geral"
    nome_aula = f"Aula de {materia} - {assunto}"

    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()

            # 1. Usuário e Turma
            usuario_id = obter_ou_criar_usuario(conn, professor_nome=professor_nome, email=professor_email)
            turma_id = obter_ou_criar_turma(conn, nome_turma=turma_nome)

            # 2. Entrada (áudio ou texto)
            cursor.execute("""
                INSERT INTO entrada (origem, caminho_arquivo, conteudo_texto, usuario_id)
                VALUES (?, ?, ?, ?)
            """, (origem, caminho_arquivo, conteudo_texto, usuario_id))
            entrada_id = cursor.lastrowid

            # 3. Aula
            cursor.execute("""
                INSERT INTO aula (nome_aula, assunto_aula, data_aula, materia_aula, observacoes_gerais, entrada_id, turma_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome_aula, assunto, data_aula, materia, None, entrada_id, turma_id))
            aula_id = cursor.lastrowid

            # 4. Provas
            for p in dados.get("provas", []):
                p_dict = p if isinstance(p, dict) else (p.model_dump() if hasattr(p, "model_dump") else p.__dict__)
                dt_prova = p_dict.get("data") or data_aula
                conteudo = p_dict.get("materia") or f"Avaliação de {materia}"
                cursor.execute("""
                    INSERT INTO prova (data_prova, conteudo_prova, aula_id)
                    VALUES (?, ?, ?)
                """, (dt_prova, conteudo, aula_id))

            # 5. Dúvidas (Ocorrência: tipo='duvida')
            for d in dados.get("duvidas", []):
                d_dict = d if isinstance(d, dict) else (d.model_dump() if hasattr(d, "model_dump") else d.__dict__)
                nome_aluno = d_dict.get("aluno") or "Aluno Não Identificado"
                descricao = d_dict.get("descricao") or "Dúvida sem descrição"
                aluno_id = obter_ou_criar_aluno(conn, nome_aluno, turma_id)
                cursor.execute("""
                    INSERT INTO ocorrencia (tipo, aluno_id, descricao, aula_id)
                    VALUES (?, ?, ?, ?)
                """, ("duvida", aluno_id, descricao, aula_id))

            # 6. Advertências (Ocorrência: tipo='advertencia')
            for a in dados.get("advertencias", []):
                a_dict = a if isinstance(a, dict) else (a.model_dump() if hasattr(a, "model_dump") else a.__dict__)
                nome_aluno = a_dict.get("aluno") or "Aluno Não Identificado"
                motivo = a_dict.get("motivo") or a_dict.get("descricao") or "Advertência sem motivo informado"
                aluno_id = obter_ou_criar_aluno(conn, nome_aluno, turma_id)
                cursor.execute("""
                    INSERT INTO ocorrencia (tipo, aluno_id, descricao, aula_id)
                    VALUES (?, ?, ?, ?)
                """, ("advertencia", aluno_id, motivo, aula_id))

        return aula_id
    finally:
        conn.close()


def consultar_resumo_aula(aula_id: int) -> Optional[Dict[str, Any]]:
    """Consulta os dados completos de uma aula e seus relacionamentos."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.id, a.nome_aula, a.assunto_aula, a.data_aula, a.materia_aula,
                   t.nome_turma, e.origem, e.conteudo_texto, u.professor_nome
            FROM aula a
            JOIN turma t ON a.turma_id = t.id
            JOIN entrada e ON a.entrada_id = e.id
            JOIN usuario u ON e.usuario_id = u.id
            WHERE a.id = ?
        """, (aula_id,))
        row = cursor.fetchone()
        if not row:
            return None

        aula_info = {
            "id": row[0],
            "nome_aula": row[1],
            "assunto": row[2],
            "data_aula": row[3],
            "materia": row[4],
            "turma": row[5],
            "origem": row[6],
            "transcricao": row[7],
            "professor": row[8],
            "provas": [],
            "ocorrencias": []
        }

        # Provas
        cursor.execute("SELECT id, data_prova, conteudo_prova FROM prova WHERE aula_id = ?", (aula_id,))
        for p in cursor.fetchall():
            aula_info["provas"].append({
                "id": p[0],
                "data_prova": p[1],
                "conteudo_prova": p[2]
            })

        # Ocorrências
        cursor.execute("""
            SELECT o.id, o.tipo, al.nome_aluno, o.descricao
            FROM ocorrencia o
            JOIN aluno al ON o.aluno_id = al.id
            WHERE o.aula_id = ?
        """, (aula_id,))
        for o in cursor.fetchall():
            aula_info["ocorrencias"].append({
                "id": o[0],
                "tipo": o[1],
                "aluno": o[2],
                "descricao": o[3]
            })

        return aula_info
    finally:
        conn.close()


if __name__ == "__main__":
    criar_tabelas()