# This is a simple test of using langgraph + vercel ai sdk. It works. But I just vibe coded it. Need to refactor.







import os
from typing_extensions import TypedDict
from typing import Annotated, List, Dict, AsyncGenerator
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import openai
import json
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Initialize client
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
router = APIRouter(prefix="/api", tags=["langgraph"])

# Define state for LangGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]

# LangGraph node: needs complete response (stream=False)
def call_model(state: State):
    # Ensure messages are properly formatted with role and content
    formatted_messages = []
    
    # Check if messages exist in state
    if "messages" in state and state["messages"]:
        for msg in state["messages"]:
            # If it's already a dict with role and content, use it as is
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                formatted_messages.append(msg)
            # If it's a string, assume it's user content
            elif isinstance(msg, str):
                formatted_messages.append({"role": "user", "content": msg})
            # If it has attributes role and content, convert to dict
            elif hasattr(msg, "role") and hasattr(msg, "content"):
                formatted_messages.append({"role": msg.role, "content": msg.content})
    
    # Ensure we have at least one message - add a default if empty
    if not formatted_messages:
        formatted_messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        # If we have a user message in state but couldn't format it, add a generic one
        if "messages" in state and state["messages"]:
            formatted_messages.append({"role": "user", "content": "Hello"})
    
    # Make API call with properly formatted messages
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=formatted_messages,
        stream=False
    )
    return {"messages": [{"role": "assistant", "content": response.choices[0].message.content}]}

# Create minimal graph
graph = StateGraph(State)
graph.add_node("llm", call_model)
graph.add_edge(START, "llm")
graph.add_edge("llm", END)
graph = graph.compile()

# Vercel AI SDK protocol formatters
async def stream_to_vercel_ai_protocol(stream) -> AsyncGenerator[str, None]:
    """Transform an OpenAI stream to Vercel AI SDK protocol format"""
    for chunk in stream:
        for choice in chunk.choices:
            if choice.delta.content is not None:
                yield f"0:{json.dumps(choice.delta.content)}\n"

        # If it's the final chunk with usage info
        if hasattr(chunk, "usage") and chunk.usage:
            yield f'e:{{"finishReason":"stop","usage":{{"promptTokens":{chunk.usage.prompt_tokens},"completionTokens":{chunk.usage.completion_tokens}}},"isContinued":false}}\n'

# FastAPI request model
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# API endpoint using LangGraph for state
@router.post("/chat")
async def chat_with_graph(request: ChatRequest):
    # Convert messages to format expected by OpenAI
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    # Ensure we have at least one message
    if not messages:
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    
    # Stream for immediate response
    stream = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=messages, 
        stream=True
    )
    
    # Update graph state in background (doesn't affect response)
    graph.invoke({"messages": messages})
    
    # Return streaming response with Vercel AI protocol
    response = StreamingResponse(stream_to_vercel_ai_protocol(stream))
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response

# CLI chat for testing
def chat_session():
    """Interactive chat with LangGraph for history and Vercel AI format for display"""
    history = [{"role": "system", "content": "You are a helpful AI assistant."}]
    print("Chat started. Type 'exit', 'quit', or 'bye' to end.")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
            
        messages = history + [{"role": "user", "content": user_input}]
        print("Assistant: ", end="", flush=True)
        
        try:
            # Stream with direct console output
            response = ""
            for chunk in client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=messages, 
                stream=True
            ):
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    response += content
            
            # Update conversation state with validated messages
            final_state = graph.invoke({"messages": messages})
            history = final_state["messages"]
            print("\n")
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        import getpass
        os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY: ")
    
    chat_session()