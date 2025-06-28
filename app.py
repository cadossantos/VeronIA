from dotenv import load_dotenv
import os
import streamlit as st

from db.db_sqlite import init_database, listar_conversas # Importar init_database e listar_conversas para o teste

load_dotenv()

# INICIALIZAÇÃO ==================================================
def inicializacao():
    """Prepara o ambiente da aplicação na inicialização.

    Esta função é crucial e executa duas tarefas principais:
    1.  `init_database()`: Garante que o banco de dados e suas tabelas
        estejam prontos para uso, criando-os se necessário.
    2.  Popula o `st.session_state`: O `session_state` é o mecanismo
        do Streamlit para manter dados persistentes entre as interações
        do usuário. Esta função define valores padrão para chaves essenciais
        (como 'memoria', 'chain', 'conversa_atual') na primeira vez que o
        usuário abre a aplicação, evitando que o estado seja perdido a cada
        ação na UI.
    """
    
    # 1. Primeiro, inicializa o banco
    try:
        init_database()
    except Exception as e:
        st.error(f"❌ Erro ao inicializar banco de dados: {e}")
        # Não usamos st.stop() aqui para permitir que o app continue, mas com erro visível.
        # O usuário precisará resolver o problema do banco para usar a funcionalidade.
        return # Sai da função inicializacao se houver erro no banco
    
    # 2. Configurações padrão do session state
    defaults = {
        'mensagens': [],
        'conversa_atual': '',
        'api_key': os.getenv("OPENAI_API_KEY", ""),
        'memoria': None, # A memória será inicializada na página do agente
        'chain': None, # A chain será inicializada na página do agente
        'modelo_nome': 'Nenhum modelo carregado',
        'provedor': 'OpenAI',  # Provedor padrão
        'modelo': 'gpt-4o-mini'  # Modelo padrão
    }
    
    # 3. Aplica os valores padrão apenas se não existirem
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    print("✅ Inicialização concluída")

# MAIN ==================================================
def main():
    """Ponto de entrada principal da aplicação Streamlit.

    Configura a página (título, ícone) e organiza o layout, definindo a
    barra lateral com suas abas e chamando a `pagina_principal` para
    renderizar o conteúdo central.
    """
    st.set_page_config(
        page_title="VeronIA",
        page_icon="🔮",
        layout="wide"
    )
    
    # Teste de erro simulado (remover após verificação)
    db_path = "db/veronia.db"
    backup_path = "db/_backup.db"
    
    if os.path.exists(db_path):
        os.rename(db_path, backup_path)
        st.warning("Simulando erro: Banco de dados renomeado para _backup.db")

    try:
        # Tenta listar conversas para forçar um erro de conexão/arquivo
        listar_conversas()
    except Exception as e:
        st.error(f"❌ Erro capturado na UI ao listar conversas: {e}")
        st.info("Este erro é esperado para o teste de simulação de falha do banco de dados.")
    finally:
        # Renomeia o banco de dados de volta
        if os.path.exists(backup_path):
            os.rename(backup_path, db_path)
            st.success("Banco de dados restaurado de _backup.db")
        
    # Inicializa tudo
    inicializacao()
    
if __name__ == '__main__':
    main()