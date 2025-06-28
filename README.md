# VeronIA

VeronIA is a web-based chat interface designed for flexible interaction with multiple Large Language Models (LLMs). It provides a clean user interface for managing conversations and switching between different AI providers, with a persistent storage backend.

## Features

The application allows users to select from various LLM providers, including OpenAI, Groq, and local models via Ollama. All conversations are automatically saved to a SQLite database (db/veronia.db), enabling users to revisit, manage, and rename past dialogues. The interface is designed for a seamless and stateful chat experience, remembering conversation history and the selected model.

## Technical Overview

The project is built with Python and leverages Streamlit for the user interface. It uses the LangChain library for LLM abstraction, which simplifies communication with different model providers. For data persistence, it uses a local SQLite database (`db/veronia.db`) accessed via Python's built-in `sqlite3` module.

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
