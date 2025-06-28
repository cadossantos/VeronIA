# VeronIA

VeronIA is a web-based chat interface designed for flexible interaction with multiple Large Language Models (LLMs). It provides a clean user interface for managing conversations and switching between different AI providers, with a persistent storage backend.

## Features

The application allows users to select from various LLM providers, including OpenAI, Groq, and local models via Ollama. All conversations are automatically saved to a PostgreSQL database, enabling users to revisit, manage, and rename past dialogues. The interface is designed for a seamless and stateful chat experience, remembering conversation history and the selected model.

## Technical Overview

The project is built with Python and leverages Streamlit for the user interface. It uses the LangChain library for LLM abstraction, which simplifies communication with different model providers. For data persistence, it connects to a PostgreSQL database using the `psycopg` driver.

## Setup and Installation

To run this project locally, you will need Python 3.11+ and Poetry installed, as well as a running PostgreSQL server.

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

    Create a `.env` file in the root directory. This file will store your database credentials and API keys. Populate it based on the following structure:

    ```
    # PostgreSQL Database Configuration
    POSTGRES_DB=your_db_name
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432

    # LLM Provider API Keys
    OPENAI_API_KEY="sk-..."
    GROQ_API_KEY="gsk_..."
    ```

4.  **Database Setup**

    Before running the application, you must manually create the database and user role in PostgreSQL. The application will create the necessary tables on its first run, but not the database or the user.

    Connect to your PostgreSQL instance (e.g., using `psql`) and run the following commands. Replace `your_db_name`, `your_db_user`, and `your_db_password` with the same values you will use in your `.env` file.

    ```sql
    CREATE DATABASE your_db_name;
    CREATE USER your_db_user WITH PASSWORD 'your_db_password';
    GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;
    ```

    **Note:** The project includes a script `db/init_db.py` for standalone table creation, but it is recommended to let the main application handle this automatically on startup.

## Running the Application

Once the setup is complete, launch the Streamlit application with the following command:

```bash
streamlit run app.py
```

The application will be available in your web browser at the local address provided by Streamlit.
