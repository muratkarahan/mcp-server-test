"""
FEC Comparison Example

Comprehensive comparison of all Forward Error Correction methods.
Demonstrates AES, Reed-Solomon, Convolutional, and NASA CCSDS standards.
"""

import sys
sys.path.insert(0, '..')

from tools.encoding_tools import (
    aes_encrypt, reed_solomon_encode, convolution_encode
)
from tools.ccsds_fec import (
    CCSDSReedSolomon, CCSDSConvolutionalCode, 
    CCSDSConcatenatedCode, CCSDSTurboCodes, CCSDSLDPCCodes,
    ccsds_fec_comparison
)
import json
import base64


def comparison_by_overhead():
    """Compare FEC methods by overhead percentage"""
    test_data = "Test Message Data"
    data_bytes = test_data.encode()
    data_bits = len(data_bytes) * 8
    
    print("=" * 80)
    print("📊 FEC Comparison: Overhead Analysis")
    print("=" * 80)
    print(f"Test Data: {test_data} ({len(data_bytes)} bytes, {data_bits} bits)")
    print()
    print("Method Comparison:")
    print("-" * 80)
    print(f"{'FEC Method':<30} {'Output':<15} {'Overhead':<15} {'Use Case':<20}")
    print("-" * 80)
    
    # AES Encryption
    result = json.loads(aes_encrypt(test_data, "testkey"))
    aes_output = len(base64.b64decode(result["ciphertext_base64"]))
    aes_overhead = ((aes_output - len(data_bytes)) / len(data_bytes) * 100)
    print(f"{'AES-256-CBC':<30} {aes_output:<15} {aes_overhead:>14.1f}% {'Encryption':<20}")
    
    # Reed-Solomon
    result = json.loads(reed_solomon_encode(test_data, 10))
    rs_output = len(base64.b64decode(result["encoded_data_base64"]))
    rs_overhead = ((rs_output - len(data_bytes)) / len(data_bytes) * 100)
    print(f"{'Reed-Solomon (nsym=10)':<30} {rs_output:<15} {rs_overhead:>14.1f}% {'Error Correction':<20}")
    
    # Convolution
    result = json.loads(convolution_encode("0" * data_bits, "7,5"))
    conv_output = len(result["encoded_bits"]) // 8
    conv_overhead = ((conv_output - len(data_bytes)) / len(data_bytes) * 100)
    print(f"{'Convolution (Rate 1/2)':<30} {conv_output:<15} {conv_overhead:>14.1f}% {'Stream Coding':<20}")
    
    # CCSDS Convolutional
    conv_codec = CCSDSConvolutionalCode("CCSDS_k3_r12")
    bits = [int(b) for b in bin(int.from_bytes(data_bytes, 'big'))[2:].zfill(data_bits)]
    conv_encoded, stats = conv_codec.encode(bits)
    conv_ccsds_output = (len(conv_encoded) + 7) // 8
    conv_ccsds_overhead = ((conv_ccsds_output - len(data_bytes)) / len(data_bytes) * 100)
    print(f"{'CCSDS Conv (K=7, 1/2)':<30} {conv_ccsds_output:<15} {conv_ccsds_overhead:>14.1f}% {'Deep Space':<20}")
    
    # CCSDS Reed-Solomon
    rs_codec = CCSDSReedSolomon("CCSDS_rs255_223")
    rs_encoded, rs_stats = rs_codec.encode(data_bytes)
    rs_ccsds_output = len(rs_encoded)
    rs_ccsds_overhead = ((rs_ccsds_output - len(data_bytes)) / len(data_bytes) * 100)
    print(f"{'CCSDS RS (255,223)':<30} {rs_ccsds_output:<15} {rs_ccsds_overhead:>14.1f}% {'Space Standard':<20}")
    
    # Concatenated
    concat_codec = CCSDSConcatenatedCode()
    concat_encoded_b64, concat_stats = concat_codec.encode(data_bytes)
    concat_output = len(base64.b64decode(concat_encoded_b64))
    concat_overhead = ((concat_output - len(data_bytes)) / len(data_bytes) * 100)
    print(f"{'Concatenated (RS+Conv)':<30} {concat_output:<15} {concat_overhead:>14.1f}% {'High Reliability':<20}")
    
    # Turbo
    turbo_codec = CCSDSTurboCodes()
    turbo_encoded_b64, turbo_stats = turbo_codec.encode(data_bytes)
    turbo_output = len(base64.b64decode(turbo_encoded_b64))
    turbo_overhead = ((turbo_output - len(data_bytes)) / len(data_bytes) * 100)
    print(f"{'Turbo Code':<30} {turbo_output:<15} {turbo_overhead:>14.1f}% {'Iterative Decoding':<20}")
    
    # LDPC
    ldpc_codec = CCSDSLDPCCodes("1/2")
    ldpc_encoded_b64, ldpc_stats = ldpc_codec.encode(data_bytes)
    ldpc_output = len(base64.b64decode(ldpc_encoded_b64))
    ldpc_overhead = ((ldpc_output - len(data_bytes)) / len(data_bytes) * 100)
    print(f"{'LDPC Code':<30} {ldpc_output:<15} {ldpc_overhead:>14.1f}% {'Modern Standard':<20}")
    
    print("-" * 80)
    print()


def comparison_by_error_correction():
    """Compare error correction capabilities"""
    
    print("=" * 80)
    print("🛡️  FEC Comparison: Error Correction Capability")
    print("=" * 80)
    print()
    
    comparisons = [
        {
            "name": "AES-256-CBC",
            "correction": "None (Encryption only)",
            "burst_protection": "No",
            "random_error": "No",
            "complexity": "Low",
            "use_case": "Confidentiality"
        },
        {
            "name": "Reed-Solomon (nsym=10)",
            "correction": "5 byte errors",
            "burst_protection": "Yes (good)",
            "random_error": "Yes (excellent)",
            "complexity": "Medium",
            "use_case": "Random errors"
        },
        {
            "name": "Convolution (Rate 1/2)",
            "correction": "Continuous",
            "burst_protection": "Yes (excellent)",
            "random_error": "Yes (good)",
            "complexity": "Medium",
            "use_case": "Burst errors"
        },
        {
            "name": "CCSDS Conv (K=7)",
            "correction": "Continuous",
            "burst_protection": "Yes (excellent)",
            "random_error": "Yes (good)",
            "complexity": "Medium",
            "use_case": "Space streams"
        },
        {
            "name": "CCSDS RS (255,223)",
            "correction": "16 byte errors",
            "burst_protection": "Yes (excellent)",
            "random_error": "Yes (excellent)",
            "complexity": "High",
            "use_case": "Block coding"
        },
        {
            "name": "Concatenated (RS+Conv)",
            "correction": "Combined strong",
            "burst_protection": "Yes (excellent)",
            "random_error": "Yes (excellent)",
            "complexity": "High",
            "use_case": "Deep space"
        },
        {
            "name": "Turbo Code",
            "correction": "Iterative",
            "burst_protection": "Yes (good)",
            "random_error": "Yes (excellent)",
            "complexity": "High",
            "use_case": "Near-Shannon"
        },
        {
            "name": "LDPC Code",
            "correction": "Iterative",
            "burst_protection": "Yes (good)",
            "random_error": "Yes (excellent)",
            "complexity": "Very High",
            "use_case": "Modern systems"
        }
    ]
    
    print(f"{'Method':<25} {'Correction':<20} {'Burst':<12} {'Random':<12} {'Complexity':<12}")
    print("-" * 80)
    for comp in comparisons:
        print(f"{comp['name']:<25} {comp['correction']:<20} {comp['burst_protection']:<12} "
              f"{comp['random_error']:<12} {comp['complexity']:<12}")
    print()


def comparison_by_use_case():
    """Compare by application use cases"""
    
    print("=" * 80)
    print("🎯 FEC Comparison: Use Cases and Applications")
    print("=" * 80)
    print()
    
    use_cases = {
        "Deep Space Communications": {
            "recommended": "Concatenated Code (RS inner + Conv outer)",
            "alternatives": ["CCSDS Turbo", "CCSDS LDPC"],
            "reason": "Near-Shannon limit performance, proven in NASA missions",
            "examples": "Mars rovers, spacecraft navigation"
        },
        "Satellite Communications": {
            "recommended": "CCSDS Reed-Solomon (255,223)",
            "alternatives": ["Concatenated", "LDPC"],
            "reason": "Industry standard, reliable byte error correction",
            "examples": "Weather satellites, communication satellites"
        },
        "Streaming Audio/Video": {
            "recommended": "Convolutional Code (Rate 1/2 or 1/3)",
            "alternatives": ["Turbo", "LDPC"],
            "reason": "Excellent burst error protection, continuous correction",
            "examples": "DVB-S, video transmission, streaming media"
        },
        "Real-time Data Links": {
            "recommended": "Convolution (Rate 1/2)",
            "alternatives": ["LDPC"],
            "reason": "Low latency, predictable processing delay",
            "examples": "Military communications, emergency services"
        },
        "Storage and Archive": {
            "recommended": "Reed-Solomon High Redundancy",
            "alternatives": ["Concatenated"],
            "reason": "Random bit error protection, no time constraint",
            "examples": "RAID systems, cloud storage, digital preservation"
        },
        "Modern 5G/6G": {
            "recommended": "LDPC Code",
            "alternatives": ["Polar codes", "Turbo"],
            "reason": "Approaching Shannon limit, efficient hardware",
            "examples": "5G cellular, next-gen wireless"
        },
        "High-Reliability Systems": {
            "recommended": "Concatenated or Turbo",
            "alternatives": ["CCSDS RS (255,223)"],
            "reason": "Strongest error correction, proven performance",
            "examples": "Medical devices, nuclear systems, avionics"
        },
        "Encryption": {
            "recommended": "AES-256-CBC",
            "alternatives": ["AES-256-GCM"],
            "reason": "Confidentiality (not error correction)",
            "examples": "Secure messaging, data protection"
        }
    }
    
    for use_case, details in use_cases.items():
        print(f"📍 {use_case}")
        print(f"   Recommended: {details['recommended']}")
        print(f"   Alternatives: {', '.join(details['alternatives'])}")
        print(f"   Reason: {details['reason']}")
        print(f"   Examples: {details['examples']}")
        print()


def comparison_by_performance():
    """Compare performance metrics"""
    
    print("=" * 80)
    print("⚡ FEC Comparison: Performance Characteristics")
    print("=" * 80)
    print()
    
    print(f"{'Method':<25} {'Overhead':<12} {'Latency':<12} {'Complexity':<12} {'Proven':<12}")
    print("-" * 80)
    
    metrics = [
        ("AES-256-CBC", "16-20%", "Very Low", "Low", "Excellent"),
        ("Reed-Solomon", "10-40%", "Low", "Medium", "Excellent"),
        ("Convolution", "100%", "Low", "Medium", "Excellent"),
        ("CCSDS Conv", "100%", "Low", "Medium", "Excellent"),
        ("CCSDS RS", "12-13%", "Low", "High", "Excellent"),
        ("Concatenated", "56%", "Medium", "High", "Excellent"),
        ("Turbo Code", "50-100%", "Medium", "High", "Good"),
        ("LDPC Code", "50-100%", "High", "Very High", "Good"),
    ]
    
    for method, overhead, latency, complexity, proven in metrics:
        print(f"{method:<25} {overhead:<12} {latency:<12} {complexity:<12} {proven:<12}")
    print()


def comparison_ccsds_focus():
    """Compare CCSDS standards for space applications"""
    
    print("=" * 80)
    print("🛰️  CCSDS Standards Comparison (NASA Space Communications)")
    print("=" * 80)
    print()
    
    print("CCSDS Standard Code Rates and Capabilities:")
    print("-" * 80)
    
    standards = [
        {
            "name": "Convolutional K=7, Rate 1/2",
            "standard": "CCSDS 131.0-B-3",
            "code_rate": "0.5 (100% overhead)",
            "correction": "Continuous bit-level",
            "use": "Streaming telemetry"
        },
        {
            "name": "Convolutional K=7, Rate 1/3",
            "standard": "CCSDS 131.0-B-3",
            "code_rate": "0.33 (200% overhead)",
            "correction": "Strong bit-level",
            "use": "High-noise environments"
        },
        {
            "name": "Reed-Solomon (255,223)",
            "standard": "CCSDS 131.0-B-3",
            "code_rate": "0.875 (12.5% overhead)",
            "correction": "16 byte errors",
            "use": "Deep space standard"
        },
        {
            "name": "Reed-Solomon (255,239)",
            "standard": "CCSDS 131.0-B-3",
            "code_rate": "0.937 (6.3% overhead)",
            "correction": "8 byte errors",
            "use": "Lighter FEC"
        },
        {
            "name": "Concatenated (RS+Conv)",
            "standard": "CCSDS 131.0-B-3",
            "code_rate": "0.44 (56% overhead)",
            "correction": "Combined maximum",
            "use": "Mars rovers, probes"
        },
        {
            "name": "Turbo Code",
            "standard": "CCSDS 131.0-B-3",
            "code_rate": "0.5 (100% overhead)",
            "correction": "Near-Shannon limit",
            "use": "Modern satellites"
        },
        {
            "name": "LDPC Code",
            "standard": "CCSDS 131.0-B-3",
            "code_rate": "0.5-0.67 (50-100% overhead)",
            "correction": "Near-Shannon limit",
            "use": "Next-generation systems"
        }
    ]
    
    print(f"{'Standard':<30} {'Code Rate':<18} {'Correction':<20} {'Primary Use':<20}")
    print("-" * 80)
    for std in standards:
        print(f"{std['name']:<30} {std['code_rate']:<18} {std['correction']:<20} {std['use']:<20}")
    print()
    
    print("Typical NASA Mission Choices:")
    print("  • Mars Rovers: Concatenated (RS inner + Conv outer) - 56% overhead")
    print("  • Deep Space Probes: CCSDS RS (255,223) - 12.5% overhead")
    print("  • Satellite Downlink: CCSDS Conv K=7 Rate 1/2 - 100% overhead")
    print("  • Future Missions: Turbo or LDPC - Near-Shannon limit")
    print()


if __name__ == "__main__":
    # Overhead Analysis
    comparison_by_overhead()
    
    # Error Correction
    comparison_by_error_correction()
    
    # Use Cases
    comparison_by_use_case()
    
    # Performance
    comparison_by_performance()
    
    # CCSDS Focus
    comparison_ccsds_focus()
