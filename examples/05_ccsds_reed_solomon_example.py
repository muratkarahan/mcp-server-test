"""
CCSDS Reed-Solomon Code Example

Demonstrates NASA CCSDS standard Reed-Solomon codes.
Industry standard for deep space communications.
"""

import sys
sys.path.insert(0, '..')

from tools.ccsds_fec import CCSDSReedSolomon
import base64


def ccsds_rs255_223_example():
    """Example: CCSDS (255,223) - Industry Standard"""
    data = "Deep Space Communication Test Data"
    standard = "CCSDS_rs255_223"
    
    # Create codec
    codec = CCSDSReedSolomon(standard)
    
    # Encode
    data_bytes = data.encode()
    encoded, stats = codec.encode(data_bytes)
    encoded_b64 = base64.b64encode(encoded).decode()
    
    print("=" * 60)
    print("🛰️ CCSDS Reed-Solomon Code (255,223)")
    print("=" * 60)
    print(f"Standard: {standard}")
    print(f"Description: {codec.config['description']}")
    print(f"Code Type: ({codec.config['n']},{codec.config['k']})")
    print()
    print(f"Original Data: {data}")
    print(f"Original Length: {len(data_bytes)} bytes")
    print(f"Parity Symbols: {stats['parity_symbols']}")
    print(f"Error Correction Capability: {stats['error_correction_capability']} bytes")
    print(f"Code Rate: {stats['code_rate']}")
    print()
    print(f"Encoded Length: {len(encoded)} bytes")
    print(f"Overhead: {((len(encoded) - len(data_bytes)) / len(data_bytes) * 100):.1f}%")
    print(f"Encoded (Base64): {encoded_b64[:50]}...")
    print()
    
    return encoded, standard


def ccsds_rs255_239_example():
    """Example: CCSDS (255,239) - Lighter Variant"""
    data = "Test Message for Satellite"
    standard = "CCSDS_rs255_239"
    
    # Create codec
    codec = CCSDSReedSolomon(standard)
    
    # Encode
    data_bytes = data.encode()
    encoded, stats = codec.encode(data_bytes)
    encoded_b64 = base64.b64encode(encoded).decode()
    
    print("=" * 60)
    print("🛰️ CCSDS Reed-Solomon Code (255,239)")
    print("=" * 60)
    print(f"Standard: {standard}")
    print(f"Description: {codec.config['description']}")
    print(f"Code Type: ({codec.config['n']},{codec.config['k']})")
    print()
    print(f"Original Data: {data}")
    print(f"Original Length: {len(data_bytes)} bytes")
    print(f"Parity Symbols: {stats['parity_symbols']}")
    print(f"Error Correction Capability: {stats['error_correction_capability']} bytes")
    print(f"Code Rate: {stats['code_rate']}")
    print()
    print(f"Encoded Length: {len(encoded)} bytes")
    print(f"Overhead: {((len(encoded) - len(data_bytes)) / len(data_bytes) * 100):.1f}%")
    print(f"Encoded (Base64): {encoded_b64[:50]}...")
    print()


def ccsds_rs_decode_example():
    """Example: Decode CCSDS Reed-Solomon data"""
    data = "Space Mission Critical Data"
    standard = "CCSDS_rs255_223"
    
    # Create codec
    codec = CCSDSReedSolomon(standard)
    
    # Encode
    data_bytes = data.encode()
    encoded, _ = codec.encode(data_bytes)
    
    # Decode
    decoded, decode_stats = codec.decode(encoded)
    
    print("=" * 60)
    print("✅ CCSDS Reed-Solomon Decoding Example")
    print("=" * 60)
    print(f"Standard: {standard}")
    print()
    print(f"Original: {data}")
    print(f"Decoded: {decoded.decode()}")
    print(f"Decoding Successful: {decoded.decode() == data}")
    print(f"Errors Corrected: {decode_stats['errors_corrected']}")
    print()


def ccsds_rs_comparison():
    """Example: Compare CCSDS Reed-Solomon standards"""
    data = "Communication Test Data"
    data_bytes = data.encode()
    
    standards = [
        ("CCSDS_rs255_223", "Deep Space Standard"),
        ("CCSDS_rs255_239", "Lighter Variant")
    ]
    
    print("=" * 60)
    print("📊 CCSDS Reed-Solomon Standards Comparison")
    print("=" * 60)
    print(f"Original Data: {data} ({len(data_bytes)} bytes)")
    print()
    
    for standard, description in standards:
        codec = CCSDSReedSolomon(standard)
        encoded, stats = codec.encode(data_bytes)
        
        print(f"{standard} - {description}:")
        print(f"  Code: ({codec.config['n']},{codec.config['k']})")
        print(f"  Parity Symbols: {stats['parity_symbols']}")
        print(f"  Error Correction: {stats['error_correction_capability']} bytes")
        print(f"  Code Rate: {stats['code_rate']}")
        print(f"  Encoded Size: {len(encoded)} bytes")
        print(f"  Overhead: {((len(encoded) - len(data_bytes)) / len(data_bytes) * 100):.1f}%")
        print()


def ccsds_rs_error_correction_example():
    """Example: Error correction capability"""
    data = "Test"
    standard = "CCSDS_rs255_223"
    
    codec = CCSDSReedSolomon(standard)
    data_bytes = data.encode()
    encoded, _ = codec.encode(data_bytes)
    
    print("=" * 60)
    print("🔧 Error Correction Capability")
    print("=" * 60)
    print(f"Standard: {standard}")
    print(f"Code: (255,223)")
    print(f"Original Data: {data} ({len(data_bytes)} bytes)")
    print()
    print(f"Can correct up to 16 byte errors in 255-byte block")
    print(f"That's error correction of: 16/255 = 6.3%")
    print()
    print(f"Encoded Block Size: {len(encoded)} bytes")
    print(f"Maximum Correctable Errors: 16 bytes")
    print()


if __name__ == "__main__":
    # CCSDS (255,223) - Industry Standard
    encoded, standard = ccsds_rs255_223_example()
    
    # CCSDS (255,239) - Lighter Variant
    ccsds_rs255_239_example()
    
    # Decoding
    ccsds_rs_decode_example()
    
    # Comparison
    ccsds_rs_comparison()
    
    # Error Correction
    ccsds_rs_error_correction_example()
