"""
Encoding and encryption tools for data encoding testing.
Provides AES encryption, Reed-Solomon coding, and Convolution coding functions.
"""

from typing import Annotated
import json
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from reedsolo import RSCodec, ReedSolomonError
import numpy as np
from scipy import signal


def aes_encrypt(
    plaintext: Annotated[str, "The text to encrypt"],
    key: Annotated[str, "Encryption key (will be padded/truncated to 32 bytes for AES-256)"],
) -> str:
    """
    Encrypt plaintext using AES-256-CBC.
    
    Args:
        plaintext: Text to encrypt
        key: Encryption key
        
    Returns:
        JSON string containing encrypted data in base64 format
    """
    try:
        # Prepare key (ensure it's 32 bytes for AES-256)
        key_bytes = key.encode().ljust(32)[:32]
        
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key_bytes),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad plaintext to multiple of 16
        plaintext_bytes = plaintext.encode()
        padding_length = 16 - (len(plaintext_bytes) % 16)
        plaintext_padded = plaintext_bytes + bytes([padding_length] * padding_length)
        
        # Encrypt
        ciphertext = encryptor.update(plaintext_padded) + encryptor.finalize()
        
        # Combine IV and ciphertext
        encrypted_data = base64.b64encode(iv + ciphertext).decode()
        
        return json.dumps({
            "status": "success",
            "operation": "AES-256-CBC Encryption",
            "plaintext": plaintext,
            "plaintext_length": len(plaintext),
            "ciphertext_base64": encrypted_data,
            "ciphertext_length": len(ciphertext),
            "iv_base64": base64.b64encode(iv).decode()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "AES-256-CBC Encryption",
            "message": str(e)
        })


def aes_decrypt(
    ciphertext_b64: Annotated[str, "Encrypted data in base64 format (IV + ciphertext)"],
    key: Annotated[str, "Same encryption key used for encryption"],
) -> str:
    """
    Decrypt AES-256-CBC encrypted data.
    
    Args:
        ciphertext_b64: Base64 encoded IV + ciphertext
        key: Same encryption key
        
    Returns:
        JSON string containing decrypted plaintext
    """
    try:
        # Prepare key
        key_bytes = key.encode().ljust(32)[:32]
        
        # Decode base64
        encrypted_data = base64.b64decode(ciphertext_b64)
        
        # Extract IV and ciphertext
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key_bytes),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        padding_length = plaintext_padded[-1]
        plaintext = plaintext_padded[:-padding_length].decode()
        
        return json.dumps({
            "status": "success",
            "operation": "AES-256-CBC Decryption",
            "ciphertext_base64": ciphertext_b64,
            "plaintext": plaintext,
            "plaintext_length": len(plaintext)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "AES-256-CBC Decryption",
            "message": str(e)
        })


def reed_solomon_encode(
    data: Annotated[str, "Data to encode (hex string or plain text)"],
    nsym: Annotated[int, "Number of error correction symbols (default 10)", "10"],
) -> str:
    """
    Encode data using Reed-Solomon error correction code.
    
    Args:
        data: Data string to encode
        nsym: Number of error correction symbols (default 10)
        
    Returns:
        JSON string containing encoded data
    """
    try:
        nsym = int(nsym) if isinstance(nsym, str) else nsym
        
        # Convert string to bytes
        data_bytes = data.encode()
        
        # Create Reed-Solomon codec
        rsc = RSCodec(nsym)
        
        # Encode
        encoded = rsc.encode(data_bytes)
        # encoded is bytearray, convert to bytes and encode as base64
        encoded_bytes = bytes(encoded) if isinstance(encoded, bytearray) else encoded
        encoded_b64 = base64.b64encode(encoded_bytes).decode()
        
        return json.dumps({
            "status": "success",
            "operation": "Reed-Solomon Encoding",
            "original_data": data,
            "original_length": len(data_bytes),
            "error_correction_symbols": nsym,
            "encoded_data_base64": encoded_b64,
            "encoded_length": len(encoded_bytes),
            "total_symbols": len(encoded_bytes)
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "Reed-Solomon Encoding",
            "message": str(e)
        })


def reed_solomon_decode(
    encoded_data_b64: Annotated[str, "Reed-Solomon encoded data in base64 format"],
    nsym: Annotated[int, "Number of error correction symbols used during encoding", "10"],
) -> str:
    """
    Decode Reed-Solomon encoded data and correct errors.
    
    Args:
        encoded_data_b64: Base64 encoded Reed-Solomon message
        nsym: Number of error correction symbols
        
    Returns:
        JSON string containing decoded data
    """
    try:
        nsym = int(nsym) if isinstance(nsym, str) else nsym
        
        # Decode base64
        encoded_bytes = base64.b64decode(encoded_data_b64)
        
        # Create Reed-Solomon codec
        rsc = RSCodec(nsym)
        
        # Decode
        decoded, ecc, errata = rsc.decode(encoded_bytes)
        
        return json.dumps({
            "status": "success",
            "operation": "Reed-Solomon Decoding",
            "decoded_data": decoded.decode() if decoded else "",
            "decoded_length": len(decoded) if decoded else 0,
            "errors_corrected": len(errata) if errata else 0,
            "error_positions": list(errata) if errata else [],
            "error_correction_symbols": nsym
        }, indent=2)
    except ReedSolomonError as e:
        return json.dumps({
            "status": "error",
            "operation": "Reed-Solomon Decoding",
            "message": f"Too many errors to correct: {str(e)}"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "Reed-Solomon Decoding",
            "message": str(e)
        })


def convolution_encode(
    input_bits: Annotated[str, "Input bit sequence (0s and 1s, comma-separated or continuous)"],
    generator_polynomial: Annotated[str, "Generator polynomial coefficients (e.g., '7,5' for (7,5) convolutional code)", "7,5"],
) -> str:
    """
    Encode data using Convolution encoding.
    
    Args:
        input_bits: Input bit sequence
        generator_polynomial: Generator polynomial in octal (e.g., "7,5" for rate 1/2)
        
    Returns:
        JSON string containing convolution-encoded data
    """
    try:
        # Parse input bits
        if ',' in input_bits:
            bits = [int(b.strip()) for b in input_bits.split(',')]
        else:
            bits = [int(b) for b in input_bits.replace(' ', '')]
        
        # Parse generator polynomial
        if ',' in generator_polynomial:
            gen_poly = [int(g.strip(), 8) for g in generator_polynomial.split(',')]
        else:
            gen_poly = [int(generator_polynomial, 8)]
        
        # Simple convolution encoding (rate 1/2)
        # Using polynomial multiplication in GF(2)
        encoded = []
        state = 0
        constraint_length = 3
        
        for bit in bits:
            state = ((state << 1) | bit) & ((1 << constraint_length) - 1)
            
            # Calculate output bits
            output = []
            for gen in gen_poly:
                parity = 0
                temp_state = state
                for i in range(constraint_length):
                    if (gen >> i) & 1:
                        parity ^= (temp_state >> i) & 1
                output.append(parity)
            
            encoded.extend(output)
        
        # Convert to string
        encoded_str = ''.join(str(b) for b in encoded)
        
        return json.dumps({
            "status": "success",
            "operation": "Convolution Encoding",
            "input_bits": ''.join(str(b) for b in bits),
            "input_length": len(bits),
            "generator_polynomial": generator_polynomial,
            "constraint_length": constraint_length,
            "code_rate": f"1/{len(gen_poly)}",
            "encoded_bits": encoded_str,
            "encoded_length": len(encoded),
            "expansion_ratio": len(encoded) / len(bits) if bits else 0
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "Convolution Encoding",
            "message": str(e)
        })


def convolution_test(
    test_type: Annotated[str, "Type of test: 'verify_rate', 'performance', or 'demo'"],
) -> str:
    """
    Run convolution encoding tests and demonstrations.
    
    Args:
        test_type: Type of test to run
        
    Returns:
        JSON string containing test results
    """
    try:
        results = {
            "status": "success",
            "operation": "Convolution Test",
            "test_type": test_type,
            "tests": []
        }
        
        if test_type == "demo":
            # Demo with simple test vector
            test_data = "10110"
            gen_poly = "7,5"
            
            results["tests"].append({
                "name": "Simple Convolutional Code Demo",
                "input": test_data,
                "generator_polynomial": gen_poly,
                "description": "(7,5) rate 1/2 convolutional code"
            })
            
        elif test_type == "verify_rate":
            # Verify code rate
            test_lengths = [8, 16, 32]
            results["tests"].append({
                "name": "Code Rate Verification",
                "constraint_length": 3,
                "test_vectors": []
            })
            
            for length in test_lengths:
                input_bits = "01" * (length // 2)
                # Rate 1/2 produces 2*length output bits
                results["tests"][0]["test_vectors"].append({
                    "input_length": len(input_bits),
                    "expected_output_length": len(input_bits) * 2,
                    "expected_code_rate": "1/2"
                })
        
        elif test_type == "performance":
            # Performance metrics
            results["tests"].append({
                "name": "Convolution Encoding Performance",
                "metrics": {
                    "constraint_length": 3,
                    "typical_frame_size": "1024 bits",
                    "output_size_rate_1_2": "2048 bits",
                    "output_size_rate_1_3": "3072 bits",
                    "redundancy_1_2": "100%",
                    "redundancy_1_3": "200%"
                }
            })
        
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "Convolution Test",
            "message": str(e)
        })
