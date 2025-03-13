"""
FastAPI application for LangManus.
"""

import json
import logging
from typing import Dict, List, Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import AsyncGenerator, Dict, List, Any

from src.graph import build_graph
from src.config import TEAM_MEMBERS

# Configure logging
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LangManus API",
    description="API for LangManus LangGraph-based agent workflow",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create the graph
graph = build_graph()


class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (user or assistant)")
    content: str = Field(..., description="The content of the message")


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="The conversation history")
    stream: bool = Field(True, description="Whether to stream the response")
    debug: Optional[bool] = Field(False, description="Whether to enable debug logging")


async def stream_graph_response(
    messages: List[Dict[str, str]], debug: bool = False
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Stream the response from the LangGraph workflow.
    
    Args:
        messages: The conversation history
        debug: Whether to enable debug logging
        
    Yields:
        The streamed response chunks
    """
    # Configure the graph for streaming
    config = {"recursion_limit": 25}
    stream_graph = graph.stream(
        {
            # Constants
            "TEAM_MEMBERS": TEAM_MEMBERS,
            # Runtime Variables
            "messages": messages,
        },
        config=config,
    )
    
    try:
        # Stream the response
        async for chunk in stream_graph:
            # Extract the relevant information from the chunk
            node = chunk.get("node")
            if node:
                yield {
                    "type": "node",
                    "node": node,
                }
            
            # If there are new messages, yield them
            state = chunk.get("state", {})
            if state and "messages" in state:
                messages = state["messages"]
                if messages and len(messages) > 0:
                    # Get the latest message
                    latest_message = messages[-1]
                    yield {
                        "type": "message",
                        "message": {
                            "role": latest_message.get("role", "assistant"),
                            "content": latest_message.get("content", ""),
                        },
                    }
    except Exception as e:
        logger.error(f"Error streaming response: {e}")
        yield {
            "type": "error",
            "error": str(e),
        }


@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint for LangGraph invoke.
    
    Args:
        request: The chat request
        
    Returns:
        The streamed response
    """
    try:
        # Convert Pydantic models to dictionaries
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # If streaming is enabled, return a streaming response
        if request.stream:
            return EventSourceResponse(
                stream_graph_response(messages, request.debug),
                media_type="text/event-stream",
            )
        
        # Otherwise, return a regular response
        result = graph.invoke(
            {
                # Constants
                "TEAM_MEMBERS": TEAM_MEMBERS,
                # Runtime Variables
                "messages": messages,
            }
        )
        
        # Extract the final messages from the result
        final_messages = result.get("messages", [])
        
        # Return the final messages
        return {
            "messages": final_messages,
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 