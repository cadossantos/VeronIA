import psycopg

conn = psycopg.connect(
    dbname="minimo",
    user="minimo",
    password="FolhadeArruda",
    host="localhost",
    port=5433
)

with conn.cursor() as cur:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversas (
        id SERIAL PRIMARY KEY,
        titulo TEXT NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        provedor TEXT,
        modelo TEXT
    );
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mensagens (
        id SERIAL PRIMARY KEY,
        conversa_id INTEGER REFERENCES conversas(id) ON DELETE CASCADE,
        role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

conn.commit()
conn.close()