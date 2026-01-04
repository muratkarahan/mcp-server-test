"""
FEC Test Agent - A WebSocket-based AI agent for testing AES, Reed-Solomon, and Convolution encoding.

This agent uses Microsoft Agent Framework for agentic conversation and communicates
via WebSocket protocol for real-time bidirectional communication.
"""

import asyncio
import os
import json
import websockets
from typing import Optional, Dict, Set
from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI
from tools.encoding_tools import (
    aes_encrypt, aes_decrypt, 
    reed_solomon_encode, reed_solomon_decode,
    convolution_encode, convolution_test
)
from tools.ccsds_fec import (
    ccsds_convolution_encode, ccsds_reed_solomon_encode,
    ccsds_concatenated_encode, ccsds_turbo_encode,
    ccsds_ldpc_encode, ccsds_fec_comparison
)


# Load environment variables
load_dotenv()

# Store active client connections and their agent threads
connected_clients: Set[websockets.WebSocketServerProtocol] = set()
client_threads: Dict[websockets.WebSocketServerProtocol, object] = {}


def get_config() -> dict:
    """Load configuration from environment variables."""
    # Ollama için bu konfigürasyon gerekli değil, local Ollama kullanıyoruz
    model_id = os.getenv("MODEL_ID", "llama3.2")
    
    return {
        "model_id": model_id
    }


async def create_fec_agent() -> ChatAgent:
    """
    Create and configure the FEC (Forward Error Correction) test agent.
    
    Returns:
        ChatAgent: Configured agent instance with encoding tools
    """
    config = get_config()
    
    # Initialize Ollama local client
    openai_client = AsyncOpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )
    
    # Create OpenAI chat client
    chat_client = OpenAIChatClient(
        async_client=openai_client,
        model_id=config["model_id"]
    )
    
    # Create agent with encoding instructions and tools
    agent = ChatAgent(
        chat_client=chat_client,
        name="FEC Test Agent",
        instructions="""You are an expert in cryptography and Forward Error Correction (FEC) coding, 
specializing in NASA CCSDS (Consultative Committee for Space Data Systems) standards.

Your role is to help users test, understand, and implement encryption and encoding techniques 
used in space communications and satellite systems.

You have access to tools for:
1. **AES Encryption**: Modern symmetric encryption (AES-256-CBC)
2. **Reed-Solomon Codes**: Classic error correction (both standard and CCSDS)
3. **Convolutional Codes**: CCSDS-compliant convolutional codes (K=7 rate 1/2, K=7 rate 1/3)
4. **Concatenated Codes**: Combined RS (inner) + Convolutional (outer) codes
5. **Turbo Codes**: Advanced iterative codes used in satellite systems
6. **LDPC Codes**: Low-Density Parity-Check codes for modern systems
7. **FEC Comparison**: Compare all methods for efficiency analysis

When users ask about CCSDS standards, use the CCSDS-specific tools.
When they ask about encryption, use AES tools.
When comparing error correction methods, use the comparison tool.

Always explain:
- Which CCSDS standard is being used
- Code rates and overhead percentages
- Error correction capability
- Best use cases (space, satellite, deep space communications)
- Performance characteristics

Provide technical details about standards compliance and performance metrics.""",
        tools=[
            # Original tools
            aes_encrypt, aes_decrypt,
            reed_solomon_encode, reed_solomon_decode,
            convolution_encode, convolution_test,
            # CCSDS FEC tools
            ccsds_convolution_encode, ccsds_reed_solomon_encode,
            ccsds_concatenated_encode, ccsds_turbo_encode,
            ccsds_ldpc_encode, ccsds_fec_comparison
        ],
    )
    
    return agent


async def handle_client(websocket: websockets.WebSocketServerProtocol, path: str):
    """Handle incoming WebSocket connections from clients."""
    agent = None
    
    try:
        # Add client to connected set
        connected_clients.add(websocket)
        
        # Create agent for this client
        agent = await create_fec_agent()
        thread = agent.get_new_thread()
        client_threads[websocket] = thread
        
        # Send welcome message
        welcome_msg = {
            "type": "welcome",
            "message": "🔐 Welcome to the FEC Test Agent!",
            "status": "ready"
        }
        await websocket.send(json.dumps(welcome_msg))
        
        print(f"✅ Client connected: {websocket.remote_address}")
        
        # Handle incoming messages
        async for message in websocket:
            try:
                data = json.loads(message)
                user_input = data.get("message", "").strip()
                
                # Skip empty input
                if not user_input:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Please enter a question or request."
                    }))
                    continue
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    await websocket.send(json.dumps({
                        "type": "farewell",
                        "message": "Thank you for testing with me! Goodbye! 👋"
                    }))
                    break
                
                # Stream response from agent
                response_text = ""
                async for chunk in agent.run_stream(user_input, thread=thread):
                    if chunk.text:
                        response_text += chunk.text
                        # Send streaming chunks
                        await websocket.send(json.dumps({
                            "type": "response_chunk",
                            "chunk": chunk.text
                        }))
                
                # Send completion message
                await websocket.send(json.dumps({
                    "type": "response_complete",
                    "total_response": response_text
                }))
                
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format. Please send a valid message."
                }))
            except Exception as e:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Error processing request: {str(e)}"
                }))
    
    except Exception as e:
        print(f"❌ Error with client {websocket.remote_address}: {str(e)}")
    
    finally:
        # Cleanup
        connected_clients.discard(websocket)
        client_threads.pop(websocket, None)
        print(f"❌ Client disconnected: {websocket.remote_address}")


async def start_websocket_server(host: str = "localhost", port: int = 8765):
    """Start the WebSocket server."""
    try:
        server = await websockets.serve(
            handle_client,
            host,
            port,
            # Allow larger messages for data encoding tests
            max_size=10 * 1024 * 1024
        )
        
        print(f"\n" + "="*60)
        print(f"🔐 FEC Test Agent WebSocket Server Started")
        print(f"="*60)
        print(f"Server running on ws://{host}:{port}")
        print(f"Waiting for connections...\n")
        
        await server.wait_closed()
    
    except Exception as e:
        print(f"❌ Server Error: {str(e)}")
        raise


async def main():
    """Main entry point."""
    port = int(os.getenv("WEBSOCKET_PORT", 8765))
    host = os.getenv("WEBSOCKET_HOST", "localhost")
    
    try:
        await start_websocket_server(host, port)
    except KeyboardInterrupt:
        print("\n\n👋 Server shutdown gracefully")
    except Exception as e:
        print(f"❌ Fatal Error: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
