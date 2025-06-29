# db/db_sqlite.py

import sqlite3
import os
import logging
import streamlit as st

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_FILE = 'db/veronia.db'

@st.cache_resource
def get_cached_conn():
    """Estabelece e retorna uma conexão com o banco de dados SQLite em cache."""
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar com o banco SQLite: {e}")
        raise

def get_conn():
    """Função legada para obter conexão. Substituída por get_cached_conn."""
    return get_cached_conn()

def init_database():
    """Garante que as tabelas do banco de dados existam.

    Executa comandos SQL `CREATE TABLE IF NOT EXISTS` para as tabelas `conversas`

    e `mensagens`. Esta abordagem idempotente garante que a aplicação possa ser

    iniciada a qualquer momento sem erros, seja na primeira vez ou em execuções

    subsequentes.

    """
    conn = get_conn()
    try:
        with conn: # Usa 'with' para garantir que a conexão seja fechada
            cursor = conn.cursor()
            # Tabela de conversas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    provedor TEXT,
                    modelo TEXT,
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Tabela de mensagens
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensagens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversa_id INTEGER,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversa_id) REFERENCES conversas(id) ON DELETE CASCADE
                );
            """)
        logging.info("Tabelas do banco SQLite verificadas/criadas com sucesso")
    except sqlite3.Error as e:
        logging.error(f"Erro ao criar tabelas SQLite: {e}")

def criar_conversa(titulo, provedor, modelo):
    """Insere uma nova conversa no banco de dados.

    Args:

        titulo (str): O título inicial para a conversa.

        provedor (str): O provedor do modelo usado na conversa (ex: 'OpenAI').

        modelo (str): O modelo específico usado (ex: 'gpt-4o-mini').

    Returns:

        int: O ID da conversa recém-criada.

    """
    conn = get_conn()
    conversa_id = None
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversas (titulo, provedor, modelo)
                VALUES (?, ?, ?);
            """, (titulo, provedor, modelo))
            conversa_id = cursor.lastrowid
    except sqlite3.Error as e:
        logging.error(f"Erro ao criar conversa SQLite: {e}")
    return conversa_id

def salvar_mensagem(conversa_id, role, content):
    """Salva uma única mensagem (do usuário ou do assistente) no banco.

    Args:

        conversa_id (int): O ID da conversa à qual a mensagem pertence.

        role (str): O autor da mensagem, deve ser 'user' ou 'assistant'.

        content (str): O conteúdo textual da mensagem.

    """
    conn = get_conn()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mensagens (conversa_id, role, content)
                VALUES (?, ?, ?);
            """, (conversa_id, role, content))
    except sqlite3.Error as e:
        logging.error(f"Erro ao salvar mensagem SQLite: {e}")

def carregar_mensagens(conversa_id):
    """Recupera todas as mensagens de uma conversa específica do banco.

    As mensagens são retornadas em ordem cronológica para reconstruir o

    histórico da conversa corretamente.

    Args:

        conversa_id (int): O ID da conversa a ser carregada.

    Returns:

        list[dict]: Uma lista de dicionários, onde cada dicionário representa

            uma mensagem com as chaves 'role' e 'content'.

    """
    conn = get_conn()
    resultados = []
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role, content
                FROM mensagens
                WHERE conversa_id = ?
                ORDER BY timestamp ASC;
            """, (conversa_id,))
            resultados = [{'role': row['role'], 'content': row['content']} for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logging.error(f"Erro ao carregar mensagens SQLite: {e}")
    return resultados

def listar_conversas():
    """Busca no banco uma lista de todas as conversas existentes.

    Retorna os dados essenciais (ID e título) para exibir na interface,

    ordenados pela data de criação para que as mais recentes apareçam primeiro.

    Returns:

        list[tuple]: Uma lista de tuplas, onde cada tupla contém (id, titulo)

            de uma conversa.

    """
    conn = get_conn()
    conversas = []
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, titulo
                FROM conversas
                ORDER BY data_criacao DESC;
            """)
            conversas = [(row['id'], row['titulo']) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        logging.error(f"Erro ao listar conversas SQLite: {e}")
    return conversas

def atualizar_titulo_conversa(conversa_id, novo_titulo):
    """Atualiza o título de uma conversa específica no banco de dados.

    Args:

        conversa_id (int): O ID da conversa a ser atualizada.

        novo_titulo (str): O novo título para a conversa.

    """
    conn = get_conn()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE conversas SET titulo = ? WHERE id = ?;
            """, (novo_titulo, conversa_id))
    except sqlite3.Error as e:
        logging.error(f"Erro ao atualizar título SQLite: {e}")

def get_titulo_conversa(conversa_id):
    """Obtém o título de uma única conversa a partir de seu ID.

    Args:

        conversa_id (int): O ID da conversa cujo título se deseja obter.

    Returns:

        str: O título da conversa, ou uma string vazia se não for encontrada.

    """
    conn = get_conn()
    titulo = ''
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT titulo FROM conversas WHERE id = ?", (conversa_id,))
            row = cursor.fetchone()
            if row:
                titulo = row['titulo']
    except sqlite3.Error as e:
        logging.error(f"Erro ao obter título SQLite: {e}")
    return titulo

def excluir_conversa(conversa_id):
    """Remove uma conversa e suas mensagens do banco de dados."""
    conn = get_conn()
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conversas WHERE id = ?", (conversa_id,))
    except sqlite3.Error as e:
        logging.error(f"Erro ao excluir conversa: {e}")
