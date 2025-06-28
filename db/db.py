# db/db.py

import psycopg
import os
# from dotenv import load_dotenv

# load_dotenv()


def get_conn():
    """Estabelece e retorna uma conexão com o banco de dados PostgreSQL.

    Lê as credenciais de conexão (usuário, senha, banco, host, porta) a
    partir das variáveis de ambiente e utiliza a biblioteca `psycopg` para
    criar a conexão.

    Returns:
        psycopg.Connection: Um objeto de conexão com o banco de dados.

    Raises:
        SystemExit: Se a conexão falhar, a função exibe uma mensagem de erro
            na interface do Streamlit e encerra a aplicação. (Nota: este
            acoplamento com a UI é um ponto de melhoria).
    """
    try:
        return psycopg.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", 5432))
        )
    except Exception as e:
        import streamlit as st
        st.error(f"❌ Erro ao conectar com o banco: {e}")
        st.error("Verifique se o PostgreSQL está rodando e as variáveis do .env estão corretas")
        st.stop()

def init_database():
    """Garante que as tabelas do banco de dados existam.

    Executa comandos SQL `CREATE TABLE IF NOT EXISTS` para as tabelas `conversas`
    e `mensagens`. Esta abordagem idempotente garante que a aplicação possa ser
    iniciada a qualquer momento sem erros, seja na primeira vez ou em execuções
    subsequentes.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Tabela de conversas
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversas (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(255) NOT NULL,
                    provedor VARCHAR(100),
                    modelo VARCHAR(100),
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Tabela de mensagens
            cur.execute("""
                CREATE TABLE IF NOT EXISTS mensagens (
                    id SERIAL PRIMARY KEY,
                    conversa_id INTEGER REFERENCES conversas(id) ON DELETE CASCADE,
                    role VARCHAR(20) NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
        print("✅ Tabelas do banco verificadas/criadas com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
    finally:
        conn.close()

        
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

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO conversas (titulo, provedor, modelo)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (titulo, provedor, modelo))
        conversa_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return conversa_id

def salvar_mensagem(conversa_id, role, content):
    """Salva uma única mensagem (do usuário ou do assistente) no banco.

    Args:
        conversa_id (int): O ID da conversa à qual a mensagem pertence.
        role (str): O autor da mensagem, deve ser 'user' ou 'assistant'.
        content (str): O conteúdo textual da mensagem.
    """
    conn = get_conn()

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO mensagens (conversa_id, role, content)
            VALUES (%s, %s, %s);
        """, (conversa_id, role, content))
    conn.commit()
    conn.close()

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

    with conn.cursor() as cur:
        cur.execute("""
            SELECT role, content
            FROM mensagens
            WHERE conversa_id = %s
            ORDER BY timestamp ASC;
        """, (conversa_id,))
        resultados = cur.fetchall()
    conn.close()
    return [{'role': r, 'content': c} for r, c in resultados]

def listar_conversas():
    """Busca no banco uma lista de todas as conversas existentes.

    Retorna os dados essenciais (ID e título) para exibir na interface,
    ordenados pela data de criação para que as mais recentes apareçam primeiro.

    Returns:
        list[tuple]: Uma lista de tuplas, onde cada tupla contém (id, titulo)
            de uma conversa.
    """
    conn = get_conn()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, titulo
            FROM conversas
            ORDER BY data_criacao DESC;
        """)
        conversas = cur.fetchall()
    conn.close()
    return conversas  # lista de tuplas (id, titulo)

def atualizar_titulo_conversa(conversa_id, novo_titulo):
    """Atualiza o título de uma conversa específica no banco de dados.

    Args:
        conversa_id (int): O ID da conversa a ser atualizada.
        novo_titulo (str): O novo título para a conversa.
    """
    conn = get_conn()

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE conversas SET titulo = %s WHERE id = %s;
        """, (novo_titulo, conversa_id))
    conn.commit()
    conn.close()

def get_titulo_conversa(conversa_id):
    """Obtém o título de uma única conversa a partir de seu ID.

    Args:
        conversa_id (int): O ID da conversa cujo título se deseja obter.

    Returns:
        str: O título da conversa, ou uma string vazia se não for encontrada.
    """
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT titulo FROM conversas WHERE id = %s", (conversa_id,))
        row = cur.fetchone()
    conn.close()
    return row[0] if row else ''
