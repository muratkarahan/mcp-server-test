"""
Reed-Solomon Error Correction Example

Demonstrates Reed-Solomon encoding and decoding with error correction.
"""

from reedsolo import RSCodec, ReedSolomonError
import base64


def reed_solomon_encode_example():
    """Example: Encode data with Reed-Solomon ECC"""
    data = "Hello, World!"
    nsym = 10  # Number of error correction symbols
    
    # Convert string to bytes
    data_bytes = data.encode()
    
    # Create Reed-Solomon codec
    rsc = RSCodec(nsym)
    
    # Encode
    encoded = rsc.encode(data_bytes)
    encoded_b64 = base64.b64encode(bytes(encoded[0])).decode()
    
    print("=" * 60)
    print("🛡️ Reed-Solomon Encoding Example")
    print("=" * 60)
    print(f"Original Data: {data}")
    print(f"Original Length: {len(data_bytes)} bytes")
    print(f"Error Correction Symbols: {nsym}")
    print(f"Max Correctable Errors: {nsym // 2} bytes")
    print(f"Encoded Length: {len(encoded[0])} bytes")
    print(f"Encoded (Base64): {encoded_b64}")
    print(f"Overhead: {((len(encoded[0]) - len(data_bytes)) / len(data_bytes) * 100):.1f}%")
    print()
    
    return encoded_b64, nsym


def reed_solomon_decode_example(encoded_data_b64, nsym):
    """Example: Decode Reed-Solomon data"""
    
    # Decode base64
    encoded_bytes = base64.b64decode(encoded_data_b64)
    
    # Create Reed-Solomon codec
    rsc = RSCodec(nsym)
    
    # Decode
    decoded, ecc, errata = rsc.decode(encoded_bytes)
    
    print("=" * 60)
    print("✅ Reed-Solomon Decoding Example")
    print("=" * 60)
    print(f"Encoded (Base64): {encoded_data_b64[:50]}...")
    print(f"Error Correction Symbols Used: {nsym}")
    print(f"Decoded Data: {decoded.decode()}")
    print(f"Decoded Length: {len(decoded)} bytes")
    print(f"Errors Corrected: {len(errata)}")
    if errata:
        print(f"Error Positions: {list(errata)}")
    print()


def reed_solomon_with_errors_example():
    """Example: Reed-Solomon error correction with corrupted data"""
    data = "Test Message 123"
    nsym = 10
    
    # Encode
    data_bytes = data.encode()
    rsc = RSCodec(nsym)
    encoded = rsc.encode(data_bytes)
    encoded_bytes = bytes(encoded[0])
    
    # Introduce errors (corrupt some bytes)
    encoded_corrupted = bytearray(encoded_bytes)
    error_positions = [5, 10, 15]  # Corrupt 3 bytes
    for pos in error_positions:
        encoded_corrupted[pos] ^= 0xFF  # Flip all bits
    
    # Decode and correct
    decoded, ecc, errata = rsc.decode(bytes(encoded_corrupted))
    
    print("=" * 60)
    print("🔧 Reed-Solomon Error Correction Example")
    print("=" * 60)
    print(f"Original Data: {data}")
    print(f"Errors Introduced: {len(error_positions)} bytes")
    print(f"Error Positions: {error_positions}")
    print(f"Errors Corrected: {len(errata)}")
    print(f"Recovered Data: {decoded.decode()}")
    print(f"Correction Successful: {decoded.decode() == data}")
    print()


if __name__ == "__main__":
    # Encode
    encoded, nsym = reed_solomon_encode_example()
    
    # Decode
    reed_solomon_decode_example(encoded, nsym)
    
    # Error Correction
    reed_solomon_with_errors_example()
