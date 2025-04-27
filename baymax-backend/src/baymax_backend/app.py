from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from baymax_backend.routers.chat import router as chat_router
# Load environment variables
load_dotenv()

# Check for OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")




# Initialize FastAPI app
app = FastAPI(title="Baymax AI Chat API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Baymax AI Chat API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("baymax_backend.app:app", host="0.0.0.0", port=8000, reload=True) 