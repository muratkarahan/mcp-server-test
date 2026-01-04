"""
CCSDS Convolutional Code Example

Demonstrates NASA CCSDS standard convolutional codes.
CCSDS 131.0-B-3: Space Data Systems
"""

import sys
sys.path.insert(0, '..')

from tools.ccsds_fec import CCSDSConvolutionalCode


def ccsds_k7_rate12_example():
    """Example: CCSDS K=7, Rate 1/2 (NASA Standard)"""
    input_bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1]
    standard = "CCSDS_k3_r12"
    
    # Create codec
    codec = CCSDSConvolutionalCode(standard)
    
    # Encode
    encoded, stats = codec.encode(input_bits)
    
    input_str = ''.join(str(b) for b in input_bits)
    encoded_str = ''.join(str(b) for b in encoded)
    
    print("=" * 60)
    print("🛰️ CCSDS Convolutional Code (K=7, Rate 1/2)")
    print("=" * 60)
    print(f"Standard: {standard}")
    print(f"Description: {codec.params['description']}")
    print(f"Generator Polynomials: [0o171, 0o133] (octal)")
    print(f"Constraint Length: {codec.params['constraint_length']}")
    print()
    print(f"Input Bits: {input_str}")
    print(f"Input Length: {len(input_bits)} bits")
    print(f"Encoded Bits: {encoded_str}")
    print(f"Encoded Length: {len(encoded)} bits")
    print(f"Code Rate: {stats['code_rate']}")
    print(f"Expansion Ratio: {stats['expansion_ratio']:.2f}x")
    print()


def ccsds_k7_rate13_example():
    """Example: CCSDS K=7, Rate 1/3 (Higher Protection)"""
    input_bits = [1, 0, 1, 1, 0, 1, 0, 0]
    standard = "CCSDS_k3_r13"
    
    # Create codec
    codec = CCSDSConvolutionalCode(standard)
    
    # Encode
    encoded, stats = codec.encode(input_bits)
    
    input_str = ''.join(str(b) for b in input_bits)
    encoded_str = ''.join(str(b) for b in encoded)
    
    print("=" * 60)
    print("🛰️ CCSDS Convolutional Code (K=7, Rate 1/3)")
    print("=" * 60)
    print(f"Standard: {standard}")
    print(f"Description: {codec.params['description']}")
    print(f"Generator Polynomials: [0o171, 0o133, 0o145] (octal)")
    print(f"Constraint Length: {codec.params['constraint_length']}")
    print()
    print(f"Input Bits: {input_str}")
    print(f"Input Length: {len(input_bits)} bits")
    print(f"Encoded Bits: {encoded_str}")
    print(f"Encoded Length: {len(encoded)} bits")
    print(f"Code Rate: {stats['code_rate']}")
    print(f"Expansion Ratio: {stats['expansion_ratio']:.2f}x")
    print()


def ccsds_k5_rate12_example():
    """Example: CCSDS K=5, Rate 1/2 (Simpler Variant)"""
    input_bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    standard = "CCSDS_k5_r12"
    
    # Create codec
    codec = CCSDSConvolutionalCode(standard)
    
    # Encode
    encoded, stats = codec.encode(input_bits)
    
    input_str = ''.join(str(b) for b in input_bits)
    encoded_str = ''.join(str(b) for b in encoded)
    
    print("=" * 60)
    print("🛰️ CCSDS Convolutional Code (K=5, Rate 1/2)")
    print("=" * 60)
    print(f"Standard: {standard}")
    print(f"Description: {codec.params['description']}")
    print(f"Generator Polynomials: [0o31, 0o27] (octal)")
    print(f"Constraint Length: {codec.params['constraint_length']}")
    print()
    print(f"Input Bits: {input_str}")
    print(f"Input Length: {len(input_bits)} bits")
    print(f"Encoded Bits: {encoded_str}")
    print(f"Encoded Length: {len(encoded)} bits")
    print(f"Code Rate: {stats['code_rate']}")
    print(f"Expansion Ratio: {stats['expansion_ratio']:.2f}x")
    print()


def ccsds_standards_comparison():
    """Example: Compare different CCSDS convolutional standards"""
    input_bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0]
    
    standards = ["CCSDS_k3_r12", "CCSDS_k3_r13", "CCSDS_k5_r12"]
    
    print("=" * 60)
    print("📊 CCSDS Standards Comparison")
    print("=" * 60)
    print(f"Input: {len(input_bits)} bits")
    print()
    
    for standard in standards:
        codec = CCSDSConvolutionalCode(standard)
        encoded, stats = codec.encode(input_bits)
        
        print(f"{standard}:")
        print(f"  Description: {codec.params['description']}")
        print(f"  Constraint Length: {stats['constraint_length']}")
        print(f"  Code Rate: {stats['code_rate']}")
        print(f"  Output: {len(encoded)} bits")
        print(f"  Overhead: {((len(encoded) / len(input_bits) - 1) * 100):.0f}%")
        print()


if __name__ == "__main__":
    # NASA Standard (K=7, Rate 1/2)
    ccsds_k7_rate12_example()
    
    # Higher Protection (K=7, Rate 1/3)
    ccsds_k7_rate13_example()
    
    # Simpler Variant (K=5, Rate 1/2)
    ccsds_k5_rate12_example()
    
    # Comparison
    ccsds_standards_comparison()
