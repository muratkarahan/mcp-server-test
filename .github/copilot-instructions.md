# FEC Test Agent - Development Guide for AI Assistants

## Project Overview
A Python-based AI agent for testing cryptographic and error correction techniques including **AES encryption**, **Reed-Solomon error correction**, and **Convolution coding**. Built with **Microsoft Agent Framework** for agentic conversation and **WebSocket** for real-time bidirectional communication with multiple clients.

## Architecture & Key Components

### Core Agent System (WebSocket-Based)
- **Main Agent Server**: [`fec_test.py`](../fec_test.py) - WebSocket server managing agent instances per client connection
- **Connection Handler**: `handle_client()` function processes each WebSocket connection independently with its own `ChatAgent` instance and persistent thread
- **Agent Creation**: Uses `ChatAgent` from `agent_framework` with `OpenAIChatClient` connecting to local Ollama server at `http://localhost:11434/v1`
- **Tool Integration**: Six callable tools injected into agent for encryption and encoding operations
- **Multi-Client Support**: Maintains separate agent threads (`client_threads` dict) for each connected WebSocket client

### Tools Layer
[`tools/encoding_tools.py`](../tools/encoding_tools.py) provides six core functions:

**AES Encryption:**
1. **`aes_encrypt(plaintext, key)`** - Encrypts text using AES-256-CBC; pads plaintext, generates random IV, returns base64 encoded (IV + ciphertext)
2. **`aes_decrypt(ciphertext_b64, key)`** - Decrypts AES-256-CBC data; extracts IV, reverses padding, returns original plaintext

**Reed-Solomon Error Correction:**
3. **`reed_solomon_encode(data, nsym)`** - Encodes data with Reed-Solomon ECC; adds `nsym` parity symbols for error correction capability
4. **`reed_solomon_decode(encoded_data_b64, nsym)`** - Decodes RS-encoded data; corrects up to `nsym/2` byte errors; returns error positions

**Convolution Coding:**
5. **`convolution_encode(input_bits, generator_polynomial)`** - Encodes bit sequence using convolutional code with specified generator polynomials; returns expanded bit stream
6. **`convolution_test(test_type)`** - Runs encoding tests: `'demo'`, `'verify_rate'`, or `'performance'` modes

[`tools/ccsds_fec.py`](../tools/ccsds_fec.py) provides NASA CCSDS FEC implementations:

**CCSDS Standards:**
1. **`ccsds_convolution_encode(input_bits, standard)`** - CCSDS-compliant convolutional codes (K=7, K=5)
2. **`ccsds_reed_solomon_encode(data, standard)`** - CCSDS RS codes: (255,223), (255,239)
3. **`ccsds_concatenated_encode(data, conv_std, rs_std)`** - RS (inner) + Convolution (outer) concatenated codes
4. **`ccsds_turbo_encode(data, frame_size)`** - CCSDS Turbo codes with iterative decoding
5. **`ccsds_ldpc_encode(data, code_rate)`** - CCSDS LDPC codes with sparse parity check matrices
6. **`ccsds_fec_comparison(test_data)`** - Compare all FEC methods for efficiency

All tools return JSON strings with structured `status`, operation details, and performance statistics.

## Critical Developer Workflows

### Running the WebSocket Server
```bash
# Prerequisites: Python 3.8+, Ollama running on localhost:11434
pip install -r requirements.txt
python fec_test.py
```

Server listens on `ws://localhost:8765` by default (configurable via `.env`)

### Client Usage Examples

**AES Encryption/Decryption:**
```javascript
const ws = new WebSocket("ws://localhost:8765");
ws.send(JSON.stringify({ 
  message: "Encrypt 'Hello World' with key 'mykey123'" 
}));
// Then: "Decrypt the result with the same key"
```

**Reed-Solomon Testing:**
```javascript
ws.send(JSON.stringify({ 
  message: "Encode 'data' using Reed-Solomon with 10 error correction symbols" 
}));
// Then: "Decode that and see if it can correct errors"
```

**Convolution Coding:**
```javascript
ws.send(JSON.stringify({ 
  message: "Encode the bits 10110 using (7,5) convolutional code" 
}));
// Then: "Run a convolution test on demo mode"
```

### Environment Setup
- Server reads `WEBSOCKET_HOST` (defaults to `localhost`) and `WEBSOCKET_PORT` (defaults to `8765`) from `.env`
- Agent reads `MODEL_ID` from `.env` (defaults to `llama3.2` if missing)
- Example `.env`:
  ```
  MODEL_ID=llama3.2
  WEBSOCKET_HOST=0.0.0.0
  WEBSOCKET_PORT=8765
  ```

### Adding New Encoding Tools
1. Define function in `tools/encoding_tools.py` with `Annotated` type hints for parameters
2. Function must return JSON string with `status` field and operation results
3. Import and add to `tools` list in `create_fec_agent()` initialization

## Project-Specific Patterns & Conventions

### Async-First WebSocket Design
- All operations are async (`async def`): agent creation, message streaming, connection handling
- Server spawns new agent instance per WebSocket connection for isolation
- Uses `asyncio.run()` for entry point; streams responses via `agent.run_stream()`
- Tool functions themselves are **synchronous** (blocking I/O acceptable for local crypto operations)

### WebSocket Message Protocol
Messages from client → server:
```json
{ "message": "user query string" }
```

Messages from server → client:
```json
{ "type": "welcome", "message": "...", "status": "ready" }
{ "type": "response_chunk", "chunk": "text fragment" }
{ "type": "response_complete", "total_response": "full text" }
{ "type": "error", "message": "error description" }
{ "type": "farewell", "message": "goodbye message" }
```

### Tool Response Format
All tools follow this JSON convention:
```python
# Success with data
{
  "status": "success",
  "operation": "AES-256-CBC Encryption",
  "plaintext": "...",
  "ciphertext_base64": "...",
  ...
}
# Error state
{
  "status": "error",
  "operation": "Operation Name",
  "message": "error description"
}
```

### Agent Instructions
Agent behavior is defined via `instructions` parameter in `ChatAgent()`. Current instructions emphasize cryptography expertise, tool explanation, and technical detail about security properties and code rates.

### Encoding Specifications

**AES-256-CBC:**
- Key: Padded/truncated to 32 bytes
- IV: Random 16 bytes
- Mode: CBC (Cipher Block Chaining)
- Padding: PKCS#7 to 16-byte blocks
- Output: Base64(IV + ciphertext)

**Reed-Solomon:**
- Uses `reedsolo` library (standard RS codec)
- Can correct up to `nsym/2` byte errors
- Typical: `nsym=10` for 5-byte error correction
- Output: Base64 encoded with error positions

**Convolution:**
- Constraint length: 3 (typical for testing)
- Rate: 1/2 (produces 2 bits per input bit) or 1/3
- Generator polynomial: Octal format (e.g., "7,5" = (7 octal, 5 octal))
- Output: Expanded bit sequence

**CCSDS Convolutional (CCSDS 131.0-B-3):**
- K=7, Rate 1/2: Generators [171, 133] octal - NASA standard
- K=7, Rate 1/3: Generators [171, 133, 145] octal
- K=5, Rate 1/2: Generators [31, 27] octal - Simpler variant

**CCSDS Reed-Solomon:**
- (255,223): 32 parity symbols, corrects 16 byte errors - Deep space standard
- (255,239): 16 parity symbols, corrects 8 byte errors - Lighter variant

**CCSDS Concatenated:**
- Inner: RS (255,223)
- Outer: Convolutional K=7 Rate 1/2
- Overall code rate: ~0.44 (56% overhead)
- Industry standard for NASA space probes

**CCSDS Turbo:**
- Frame size: 6144 bits
- Iterative decoding architecture
- Code rate: 1/2
- Near Shannon limit performance

**CCSDS LDPC:**
- Sparse parity-check matrices
- Code rate: 1/2 or 1/3
- Modern satellite standard
- Low complexity decoding

## Integration Points & Dependencies

### External Dependencies
- `agent-framework-azure-ai>=0.0.1rc1` - Microsoft agent orchestration
- `openai>=1.3.0` - OpenAI client for Ollama communication
- `websockets>=12.0` - WebSocket server protocol
- `cryptography>=41.0.0` - AES encryption (standard library wrapper)
- `reedsolo>=1.7.0` - Reed-Solomon codec implementation
- `numpy>=1.24.0` - Numeric operations for convolution
- `scipy>=1.11.0` - Signal processing utilities
- `python-dotenv>=1.0.0` - Environment variable loading

### Ollama Integration
- Agent connects via `AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")`
- Ollama must be running and reachable; connection errors surface during agent creation
- Model selection via `MODEL_ID` env variable

### Agent Framework Patterns
- `ChatAgent` auto-handles tool invocation based on query semantics
- Streaming response chunks via `agent.run_stream()` yield objects with `.text` property
- Framework intelligently matches user queries to encoding tools

## Common Modifications

**To add new cryptographic algorithm**: Create function in `encoding_tools.py` with `Annotated` parameters, add to agent tools list

**To add CCSDS FEC**: Create class in `ccsds_fec.py`, add tool function with `Annotated` parameters

**To increase RS error correction**: Increase `nsym` parameter (but limits data payload)

**To test different convolutional codes**: Modify generator polynomial arguments in test functions

**To benchmark encoding performance**: Use `convolution_test()` with `'performance'` mode; extend with timing measurements

**To use different CCSDS standards**: Call functions with different `standard` parameter:
- Convolutional: "CCSDS_k3_r12", "CCSDS_k3_r13", "CCSDS_k5_r12"
- Reed-Solomon: "CCSDS_rs255_223", "CCSDS_rs255_239"

## CCSDS Standards Reference

NASA CCSDS 131.0-B-3 defines FEC for space communications:
- **Convolutional**: For streaming applications, rate 1/2 or 1/3
- **Reed-Solomon**: For block-coded data, variable error correction
- **Concatenated**: RS inner + Conv outer for near-Shannon performance
- **Turbo Codes**: Iterative decoding, used in modern satellites
- **LDPC**: Sparse matrices, approaching Shannon limit

## Testing & Debugging

- Server catches tool execution errors and sends them as `error` type messages
- `KeyboardInterrupt` (Ctrl+C) exits server cleanly
- Invalid JSON from client triggers `error` type response
- Configuration errors (missing Ollama) surface immediately on first client connection
- Base64 encoding handles binary data safely for JSON transmission
- Use `wscat` for manual WebSocket testing:
  ```bash
  npm install -g wscat
  wscat -c ws://localhost:8765
  # Try: { "message": "Encrypt hello with key test" }
  ```
