# Baymax

A project combining a FastAPI backend with a React/Expo frontend. The backend streams open ai LLM response and formats endpoints for the Vercel AI SDK to enable streaming chat responses.

**Note:** You need to configure your OpenAI API key. You can either set it up in a `.env` file in the backend directory or have it configured in your shell environment (e.g., `~/.bashrc`).

## API Routes

The FastAPI backend provides the routes in these files:
- `chat.py`: A basic route using only the OpenAI API 


## Setup and Running

Follow these steps to set up and run the project: Run both servers in separate terminals at the same time.

### Backend (`baymax-backend/`)

1.  **Navigate to the backend directory:**
    ```bash
    cd baymax-backend
    ```

2.  **Install Poetry** (if you haven't already):
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3.  **Create and configure the `.env` file:**
    Create a file named `.env` in the `baymax-backend` directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    ```
    *(Alternatively, ensure `OPENAI_API_KEY` is set as an environment variable in your shell.)*

4.  **Install dependencies:**
    ```bash
    poetry install
    ```

5.  **Activate the virtual environment:**
    ```bash
    poetry env activate
    ``` 
   

6.  **Run the backend server:**
    ```bash
    poetry run uvicorn src.baymax_backend.app:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

### Frontend (`baymax_frontend/`)

1.  **Navigate to the frontend directory:**
    ```bash
    # Make sure you are in the project root before running this
    cd baymax_frontend 
    ```
    *(If you are already in the `baymax-backend` directory, use `cd ../baymax_frontend`)*

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Start the development server:**
    ```bash
    npm run start
    ```

4.  **Open the app:**
    - Press `w` in the terminal to open the web version in your browser.
    - Alternatively, scan the QR code using the Expo Go app on your mobile device. (**for this, you need to setup your computer's local IP address in the util.ts file**)

## Project Structure

-   `baymax-backend/`: Contains the FastAPI backend code, including LangGraph integration.
-   `baymax_frontend/`: Contains the React/Expo frontend application code.



