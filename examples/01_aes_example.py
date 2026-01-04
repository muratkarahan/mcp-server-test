"""
AES-256-CBC Encryption Example

Demonstrates AES encryption/decryption with CBC mode.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64


def aes_encrypt_example():
    """Example: Encrypt a message with AES-256-CBC"""
    plaintext = "Hello, this is a secret message!"
    key = "my_secret_key_12345"
    
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
    
    print("=" * 60)
    print("🔐 AES-256-CBC Encryption Example")
    print("=" * 60)
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Plaintext Length: {len(plaintext)} bytes")
    print(f"Encrypted (Base64): {encrypted_data}")
    print(f"Encrypted Length: {len(base64.b64decode(encrypted_data))} bytes")
    print()
    
    return encrypted_data, key


def aes_decrypt_example(ciphertext_b64, key):
    """Example: Decrypt an AES-256-CBC message"""
    
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
    
    print("=" * 60)
    print("🔓 AES-256-CBC Decryption Example")
    print("=" * 60)
    print(f"Encrypted (Base64): {ciphertext_b64}")
    print(f"Key: {key}")
    print(f"Decrypted: {plaintext}")
    print()


if __name__ == "__main__":
    # Encrypt
    encrypted, key = aes_encrypt_example()
    
    # Decrypt
    aes_decrypt_example(encrypted, key)
