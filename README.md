# FEC Test Agent

A WebSocket-based AI agent for testing Forward Error Correction (FEC) techniques including AES encryption, Reed-Solomon error correction, and Convolution coding.

## Features

- **AES-256-CBC Encryption**: Encrypt and decrypt data with AES
- **Reed-Solomon Error Correction**: Encode data with ECC for error correction
- **Convolution Coding**: Test convolutional codes with configurable generator polynomials
- **WebSocket Communication**: Real-time bidirectional communication with multiple clients
- **Powered by Local Ollama**: Uses local language model inference

## Prerequisites

- Python 3.8+
- Ollama running on localhost:11434
- Access to local models (e.g., llama3.2)

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env`:
   ```
   MODEL_ID=llama3.2
   WEBSOCKET_HOST=0.0.0.0
   WEBSOCKET_PORT=8765
   ```

## Usage

Run the FEC test agent server:

```bash
python fec_test.py
```

Then connect with a WebSocket client and send messages:
- "Encrypt 'Hello World' with key 'mykey123'"
- "Decode 'data' using Reed-Solomon with 10 error correction symbols"
- "Encode the bits 10110 using (7,5) convolutional code"
- "Run a convolution test on demo mode"

Type `exit` or `quit` to end the conversation.

## Project Structure

## Project Structure

```
.
├── requirements.txt              # Python dependencies
├── .env.example                 # Environment variables template
├── README.md                    # This file
├── fec_test.py                  # Main FEC test agent application
└── tools/
    ├── __init__.py
    ├── encoding_tools.py        # Basic encryption and encoding tools
    └── ccsds_fec.py             # NASA CCSDS FEC implementations
```

## Architecture

The application uses:
- **Microsoft Agent Framework**: For agent orchestration and multi-turn conversations
- **Local Ollama**: For AI language model inference
- **WebSocket**: For real-time client communication
- **Cryptography Libraries**: For encryption and error correction

## Supported Encoding Techniques

### Basic Encryption & Coding
- **AES-256-CBC**: 256-bit symmetric encryption with CBC mode
- **Reed-Solomon**: Configurable error correction, up to 255-symbol codes
- **Convolutional**: K=3 constraint length, rate 1/2 and 1/3

### NASA CCSDS (Consultative Committee for Space Data Systems) FEC Standards

#### CCSDS Convolutional Codes (CCSDS 131.0-B-3)
- **CCSDS_k3_r12**: K=7, Rate 1/2 - NASA standard for space communications
  - Generator polynomials: [171, 133] octal
  - Constraint length: 7
- **CCSDS_k3_r13**: K=7, Rate 1/3 - Higher protection variant
- **CCSDS_k5_r12**: K=5, Rate 1/2 - Simpler alternative

#### CCSDS Reed-Solomon Codes
- **(255,223)**: Industry standard for space
  - 32 parity symbols, corrects up to 16 byte errors
  - Used in deep space missions
- **(255,239)**: Lighter variant for less critical applications
  - 16 parity symbols, corrects up to 8 byte errors

#### CCSDS Concatenated Codes
- Inner code: Reed-Solomon (255,223)
- Outer code: Convolutional (K=7, Rate 1/2)
- Standard for NASA space probes and satellites
- Achieves near Shannon limit performance

#### CCSDS Turbo Codes
- Iterative decoding architecture
- Frame size: 6144 bits (standard)
- Code rate: 1/2 or 1/3
- Used in modern satellite downlinks

#### CCSDS LDPC Codes
- Low-Density Parity-Check codes
- Sparse matrix structure
- Approaching Shannon limit
- Code rates: 1/2, 1/3
- Next-generation space communication standard

## Notes

- The agent uses local Ollama for inference (no API tokens needed)
- Conversation context is maintained within a WebSocket session using Agent Framework's thread feature
- Each client connection gets its own independent agent instance
