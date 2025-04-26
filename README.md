# Baymax

A project with a FastAPI backend and React/Expo frontend. The backend utilizes LangGraph with endpoints formatted for Vercel AI SDK, so that we can stream the response in the chat.

## API Routes

The FastAPI backend currently has two routes:
- A basic route that only uses the OpenAI API (not used in the app anymore)
- A route using LangGraph (currently needs refactoring as I just vibe coded it)

## Demo


<!-- HTML video embed for better compatibility -->
<video width="640" height="360" controls>
  <source src="demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

## Setup and Running

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd baymax-backend
   ```

2. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Run the backend server:
   ```bash
   # Using Poetry to run the server
   poetry run uvicorn src.baymax_backend.app:app --reload
   
   # Alternative: Activate the virtual environment and run directly app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd baymax_frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run start
   ```

4. Press `w` to open the web version of the app. Or use expo go to scan the QR code and open the app on your phone.

## Project Structure

- `baymax-backend/`: FastAPI backend with LangGraph integration
- `baymax_frontend/`: React/Expo frontend application



