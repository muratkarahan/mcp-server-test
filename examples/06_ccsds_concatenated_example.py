"""
CCSDS Concatenated Code Example

Demonstrates NASA CCSDS concatenated codes.
Reed-Solomon (inner) + Convolutional (outer) for near-Shannon limit performance.
Used in NASA space probes and deep space communications.
"""

import sys
sys.path.insert(0, '..')

from tools.ccsds_fec import CCSDSConcatenatedCode
import base64


def concatenated_code_basic_example():
    """Example: Basic Concatenated Code Encoding"""
    data = "NASA Deep Space Message"
    
    # Create concatenated codec
    codec = CCSDSConcatenatedCode(
        conv_standard="CCSDS_k3_r12",
        rs_standard="CCSDS_rs255_223"
    )
    
    # Encode
    data_bytes = data.encode()
    encoded_b64, stats = codec.encode(data_bytes)
    
    print("=" * 70)
    print("🛰️ CCSDS Concatenated Code (RS inner + Conv outer)")
    print("=" * 70)
    print()
    print("Encoding Architecture:")
    print("  Inner Code: Reed-Solomon (255,223)")
    print("    - Adds 32 parity symbols")
    print("    - Corrects up to 16 byte errors")
    print("  Outer Code: Convolutional K=7, Rate 1/2")
    print("    - Constraint Length: 7")
    print("    - Doubles the bit stream")
    print()
    print(f"Original Data: {data}")
    print(f"Original Size: {stats['original_data_length']} bytes")
    print()
    print("Encoding Process:")
    print(f"1. RS Encode: {stats['original_data_length']} → {stats['rs_encoded_length']} bytes")
    print(f"2. Convert to Bits: {stats['rs_encoded_length']} bytes → {stats['rs_encoded_length'] * 8} bits")
    print(f"3. Conv Encode: {stats['rs_encoded_length'] * 8} bits → {stats['total_bits']} bits (rate 1/2)")
    print(f"4. Convert to Bytes: {stats['total_bits']} bits → {stats['output_length']} bytes")
    print()
    print(f"Output Size: {stats['output_length']} bytes")
    print(f"Total Overhead: {((stats['output_length'] - stats['original_data_length']) / stats['original_data_length'] * 100):.1f}%")
    print(f"Overall Code Rate: {stats['overall_code_rate']:.3f}")
    print(f"Encoded (Base64): {encoded_b64[:40]}...")
    print()


def concatenated_code_nasa_standards():
    """Example: NASA Standard Concatenated Codes"""
    data = "NASA Space Communication"
    
    configurations = [
        ("CCSDS_k3_r12", "CCSDS_rs255_223", "Deep Space Standard"),
        ("CCSDS_k3_r13", "CCSDS_rs255_223", "Stronger Outer Code"),
        ("CCSDS_k3_r12", "CCSDS_rs255_239", "Lighter RS"),
    ]
    
    print("=" * 70)
    print("📊 NASA Standard Concatenated Code Configurations")
    print("=" * 70)
    print(f"Test Data: {data} ({len(data.encode())} bytes)")
    print()
    
    for conv_std, rs_std, description in configurations:
        codec = CCSDSConcatenatedCode(conv_std, rs_std)
        encoded_b64, stats = codec.encode(data.encode())
        
        print(f"{description}:")
        print(f"  Outer (Conv): {conv_std}")
        print(f"  Inner (RS): {rs_std}")
        print(f"  Original: {stats['original_data_length']} bytes")
        print(f"  Encoded: {stats['output_length']} bytes")
        print(f"  Overhead: {((stats['output_length'] - stats['original_data_length']) / stats['original_data_length'] * 100):.1f}%")
        print(f"  Code Rate: {stats['overall_code_rate']:.3f}")
        print()


def concatenated_code_performance():
    """Example: Performance Analysis"""
    
    print("=" * 70)
    print("⚡ Concatenated Code Performance Analysis")
    print("=" * 70)
    print()
    
    print("NASA Space Probe Configuration:")
    print("  Outer Code: Convolutional K=7, Rate 1/2")
    print("  Inner Code: Reed-Solomon (255,223)")
    print()
    
    print("Performance Characteristics:")
    print("  • Overall Code Rate: ~0.44 (56% redundancy)")
    print("  • Combined Error Correction: Powerful")
    print("    - RS corrects byte errors in blocks")
    print("    - Conv provides protection against burst errors")
    print("  • Processing Complexity: Medium")
    print("  • Decoding Delay: Low (suitable for real-time)")
    print()
    
    print("Best Use Cases:")
    print("  ✓ Deep space communications (Mars, Jupiter, Saturn)")
    print("  ✓ Long-distance satellite transmissions")
    print("  ✓ Critical mission data with high reliability")
    print("  ✓ When near-Shannon limit performance needed")
    print()
    
    print("Typical Frame Structure:")
    print("  • Input: 223 bytes of data")
    print("  • RS adds: 32 parity bytes → 255 bytes")
    print("  • Convert to bits: 255 × 8 = 2040 bits")
    print("  • Conv encodes: 2040 × 2 = 4080 bits (rate 1/2)")
    print("  • Output: 510 bytes")
    print("  • Efficiency: 223/510 = 43.7%")
    print()


def concatenated_code_real_world():
    """Example: Real-world mission scenario"""
    mission_data = "PERSEVERANCE: Status OK, Position 38.2, Battery 87%"
    
    codec = CCSDSConcatenatedCode()
    data_bytes = mission_data.encode()
    encoded_b64, stats = codec.encode(data_bytes)
    
    print("=" * 70)
    print("🔴 Real-World Scenario: Mars Rover Communication")
    print("=" * 70)
    print()
    
    print("Message from Mars Perseverance Rover:")
    print(f"  {mission_data}")
    print()
    
    print("Transmission via Concatenated Code:")
    print(f"  Original Message: {len(data_bytes)} bytes")
    print(f"  RS Encoding: +32 parity bytes (error correction)")
    print(f"  Conv Encoding: ×2 bits (protection against burst errors)")
    print(f"  Final Size: {stats['output_length']} bytes")
    print()
    
    print("Advantages for Mars Communication:")
    print("  • 140+ million miles distance → high noise environment")
    print("  • Concatenated code combats both burst and random errors")
    print("  • RS inner code: handles byte-level corruption")
    print("  • Conv outer code: handles bit-level errors")
    print("  • Together: near-Shannon limit performance (~0.5 dB from limit)")
    print()


def concatenated_code_components():
    """Example: Understanding the components"""
    
    print("=" * 70)
    print("🔍 Concatenated Code Component Analysis")
    print("=" * 70)
    print()
    
    print("Inner Code: Reed-Solomon (255,223)")
    print("  • Works on: 223-byte data blocks")
    print("  • Output: 255-byte encoded blocks")
    print("  • Correction: Up to 16 byte errors per block")
    print("  • Best against: Random/isolated byte errors")
    print("  • Overhead: 32/255 = 12.5% per block")
    print()
    
    print("Outer Code: Convolutional K=7, Rate 1/2")
    print("  • Works on: Bit streams from RS encoder")
    print("  • Expansion: Doubles the number of bits")
    print("  • Memory: 7-bit constraint length (6-bit state)")
    print("  • Best against: Burst errors")
    print("  • Overhead: 100% (every bit doubled)")
    print()
    
    print("Combined Effect:")
    print("  • RS handles byte-level errors")
    print("  • Conv handles bit-level and burst errors")
    print("  • Interleaving can improve burst error performance")
    print("  • Total overhead: 56% for deep space standard")
    print()


if __name__ == "__main__":
    # Basic Example
    concatenated_code_basic_example()
    
    # NASA Standards
    concatenated_code_nasa_standards()
    
    # Performance
    concatenated_code_performance()
    
    # Real-world Scenario
    concatenated_code_real_world()
    
    # Component Analysis
    concatenated_code_components()
