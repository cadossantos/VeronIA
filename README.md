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

4.  **Database Initialization**

    The application will attempt to create the necessary tables (`conversas`, `mensagens`) on its first run. Ensure the database specified in your `.env` file exists and the user has permission to create tables.

## Running the Application

Once the setup is complete, launch the Streamlit application with the following command:

```bash
streamlit run app.py
```

The application will be available in your web browser at the local address provided by Streamlit.
