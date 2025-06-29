# VeronIA

VeronIA is a web-based chat interface designed for flexible interaction with multiple Large Language Models (LLMs). It provides a clean user interface for managing conversations and switching between different AI providers, with a persistent storage backend.

## Features

The application allows users to select from various LLM providers, including OpenAI, Groq, and local models via Ollama. All conversations are automatically saved to a SQLite database (db/veronia.db), enabling users to revisit, manage, and rename past dialogues. The interface is designed for a seamless and stateful chat experience, remembering conversation history and the selected model.

## Technical Overview

The project is built with Python and Streamlit, following a modular architecture that separates concerns into different components:

- **`pages/`**: Contains the main chat interface page (`_Chat_Geral.py`).
- **`components/`**: Reusable Streamlit components for the UI (header, sidebar, chat display).
- **`services/`**: Business logic for managing conversations, models, and memory.
- **`db/`**: Data access layer, exclusively using a local SQLite database (`db/veronia.db`) via the `db_sqlite.py` module.
- **`utils/`**: Utility functions for configuration and session state management.

This structure leverages LangChain for LLM abstraction and Python's built-in `sqlite3` for persistence, requiring no external database server.

## Setup and Installation

To run this project locally, you will need Python 3.11+ and Poetry installed. A database server is not required because SQLite is used.

1.  **Clone the repository**

    ```bash
    git clone <repository-url>
    cd minimo
    ```

2.  **Install dependencies**

    This project uses Poetry for dependency management. Install the required packages with the following command:

    ```bash
    poetry install
    ```

    The `pyproject.toml` file is the single source of truth for dependencies. A
    `requirements.txt` is not included to avoid version mismatches. If you need
    a requirements file for deployment, generate one with:

    ```bash
    poetry export --without-hashes > requirements.txt
    ```

3.  **Configure Environment Variables**

    Create a `.env` file in the root directory to store your LLM provider API keys:


    # LLM Provider API Keys
    OPENAI_API_KEY="sk-..."
    GROQ_API_KEY="gsk_..."
    ```

No manual database setup is required. The application uses a local SQLite database stored at `db/veronia.db`. The function `init_database()` will create the necessary tables on first run.


## Running the Application

Once the setup is complete, launch the Streamlit application with the following command:

```bash
streamlit run app.py
```

The application will be available in your web browser at the local address provided by Streamlit.

## License

This project is licensed under the terms of the GNU General Public License v3.0.
See the [LICENSE](LICENSE) file for details.
