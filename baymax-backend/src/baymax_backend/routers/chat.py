from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, AsyncGenerator
import openai
import os
import json


# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter(prefix="/api", tags=["chat"])


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


async def stream_to_vercel_ai_protocol(stream) -> AsyncGenerator[str, None]:
    """Transform an OpenAI stream to Vercel AI SDK protocol format"""
    for chunk in stream:
        for choice in chunk.choices:
            if choice.delta.content is not None:
                yield f"0:{json.dumps(choice.delta.content)}\n"

        # If it's the final chunk with usage info
        if hasattr(chunk, "usage") and chunk.usage:
            yield f'e:{{"finishReason":"stop","usage":{{"promptTokens":{chunk.usage.prompt_tokens},"completionTokens":{chunk.usage.completion_tokens}}},"isContinued":false}}\n'


def create_vercel_ai_streaming_response(stream) -> StreamingResponse:
    """Create a FastAPI StreamingResponse using Vercel AI protocol"""
    response = StreamingResponse(stream_to_vercel_ai_protocol(stream))
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


@router.post("/chat")
async def chat(request: ChatRequest, protocol: str = Query("data")):
    try:
        print("request", request)
        # Convert the messages to the format expected by OpenAI
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        # Create a streaming response using OpenAI
        stream = client.chat.completions.create(
            model="gpt-4o", messages=messages, stream=True
        )

        # Stream the response back to the client using Vercel AI SDK protocol
        return create_vercel_ai_streaming_response(stream)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
