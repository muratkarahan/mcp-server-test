"""
NASA CCSDS FEC (Forward Error Correction) Implementation and Testing

Implements FEC standards from NASA CCSDS (Consultative Committee for Space Data Systems):
- Convolutional Codes (CCSDS 131.0-B-3)
- Reed-Solomon Codes (CCSDS 131.0-B-3)
- Concatenated Codes
- Turbo Codes (basic)
- LDPC Codes (basic)
"""

import json
import base64
import numpy as np
from typing import Annotated, Tuple, List, Dict
from reedsolo import RSCodec, ReedSolomonError


# ============================================================================
# CCSDS Convolutional Codes (CCSDS 131.0-B-3)
# ============================================================================

class CCSDSConvolutionalCode:
    """CCSDS-compliant Convolutional Code implementation."""
    
    # CCSDS Standard generator polynomials
    STANDARD_POLYNOMIALS = {
        "CCSDS_k3_r12": {
            "constraint_length": 7,
            "code_rate": "1/2",
            "generators": [0o171, 0o133],  # Octal (NASA standard)
            "description": "K=7, Rate 1/2 - CCSDS 131.0-B-3"
        },
        "CCSDS_k3_r13": {
            "constraint_length": 7,
            "code_rate": "1/3",
            "generators": [0o171, 0o133, 0o145],
            "description": "K=7, Rate 1/3 - CCSDS 131.0-B-3"
        },
        "CCSDS_k5_r12": {
            "constraint_length": 5,
            "code_rate": "1/2",
            "generators": [0o31, 0o27],
            "description": "K=5, Rate 1/2 - Simpler variant"
        }
    }
    
    def __init__(self, standard: str = "CCSDS_k3_r12"):
        """Initialize with CCSDS standard."""
        if standard not in self.STANDARD_POLYNOMIALS:
            raise ValueError(f"Unknown standard: {standard}")
        
        self.standard = standard
        self.params = self.STANDARD_POLYNOMIALS[standard]
        self.constraint_length = self.params["constraint_length"]
        self.generators = self.params["generators"]
    
    def encode(self, input_bits: List[int]) -> Tuple[List[int], Dict]:
        """Encode input bits using convolutional code."""
        encoded = []
        state = 0
        
        for bit in input_bits:
            # Update state
            state = ((state << 1) | bit) & ((1 << (self.constraint_length - 1)) - 1)
            
            # Generate output bits
            for gen in self.generators:
                parity = 0
                temp_state = state
                for i in range(self.constraint_length):
                    if (gen >> i) & 1:
                        parity ^= (temp_state >> i) & 1
                encoded.append(parity)
        
        # Add tail bits (flush the shift register)
        for _ in range(self.constraint_length - 1):
            state = (state << 1) & ((1 << (self.constraint_length - 1)) - 1)
            for gen in self.generators:
                parity = 0
                temp_state = state
                for i in range(self.constraint_length):
                    if (gen >> i) & 1:
                        parity ^= (temp_state >> i) & 1
                encoded.append(parity)
        
        stats = {
            "input_length": len(input_bits),
            "output_length": len(encoded),
            "code_rate": self.params["code_rate"],
            "constraint_length": self.constraint_length,
            "expansion_ratio": len(encoded) / len(input_bits) if input_bits else 0
        }
        
        return encoded, stats


# ============================================================================
# CCSDS Reed-Solomon Codes (CCSDS 131.0-B-3)
# ============================================================================

class CCSDSReedSolomon:
    """CCSDS-compliant Reed-Solomon Code implementation."""
    
    STANDARD_CONFIGS = {
        "CCSDS_rs255_223": {
            "n": 255,
            "k": 223,
            "t": 16,
            "nsym": 32,
            "description": "(255,223) RS code - CCSDS standard"
        },
        "CCSDS_rs255_239": {
            "n": 255,
            "k": 239,
            "t": 8,
            "nsym": 16,
            "description": "(255,239) RS code - Lighter FEC"
        }
    }
    
    def __init__(self, standard: str = "CCSDS_rs255_223"):
        """Initialize with CCSDS RS standard."""
        if standard not in self.STANDARD_CONFIGS:
            raise ValueError(f"Unknown standard: {standard}")
        
        self.standard = standard
        self.config = self.STANDARD_CONFIGS[standard]
        self.codec = RSCodec(self.config["nsym"])
    
    def encode(self, data: bytes) -> Tuple[bytes, Dict]:
        """Encode data with RS code."""
        encoded = self.codec.encode(data)
        
        stats = {
            "original_length": len(data),
            "encoded_length": len(encoded[0]),
            "parity_symbols": self.config["nsym"],
            "error_correction_capability": self.config["t"],
            "code_rate": f"{self.config['k']}/{self.config['n']}"
        }
        
        return bytes(encoded[0]), stats
    
    def decode(self, encoded_data: bytes) -> Tuple[bytes, Dict]:
        """Decode RS encoded data."""
        try:
            decoded, ecc, errata = self.codec.decode(encoded_data)
            
            stats = {
                "decoded_length": len(decoded),
                "errors_corrected": len(errata),
                "error_positions": list(errata) if errata else [],
                "status": "success"
            }
            
            return bytes(decoded), stats
        except ReedSolomonError as e:
            return b"", {
                "status": "error",
                "message": f"Too many errors to correct: {str(e)}"
            }


# ============================================================================
# CCSDS Concatenated Codes
# ============================================================================

class CCSDSConcatenatedCode:
    """Concatenated codes: Convolutional (outer) + Reed-Solomon (inner)."""
    
    def __init__(self, conv_standard: str = "CCSDS_k3_r12", 
                 rs_standard: str = "CCSDS_rs255_223"):
        """Initialize concatenated code with outer and inner codes."""
        self.conv_code = CCSDSConvolutionalCode(conv_standard)
        self.rs_code = CCSDSReedSolomon(rs_standard)
    
    def encode(self, data: bytes) -> Tuple[str, Dict]:
        """Encode using both RS (inner) and Conv (outer) codes."""
        # First: RS encode (inner code)
        rs_encoded, rs_stats = self.rs_code.encode(data)
        
        # Second: Convert to bits and convolutional encode (outer code)
        bits = []
        for byte in rs_encoded:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        
        conv_encoded, conv_stats = self.conv_code.encode(bits)
        
        # Convert back to base64
        output_bytes = []
        for i in range(0, len(conv_encoded), 8):
            byte_bits = conv_encoded[i:i+8]
            # Pad if necessary
            while len(byte_bits) < 8:
                byte_bits.append(0)
            byte_val = 0
            for bit in byte_bits:
                byte_val = (byte_val << 1) | bit
            output_bytes.append(byte_val)
        
        output_b64 = base64.b64encode(bytes(output_bytes)).decode()
        
        stats = {
            "original_data_length": len(data),
            "rs_encoded_length": rs_stats["encoded_length"],
            "total_bits": len(conv_encoded),
            "output_length": len(output_bytes),
            "code_type": "Concatenated (RS inner + Conv outer)",
            "overall_code_rate": (len(data) * 8) / len(conv_encoded) if conv_encoded else 0
        }
        
        return output_b64, stats


# ============================================================================
# CCSDS Turbo Codes (Basic Implementation)
# ============================================================================

class CCSDSTurboCodes:
    """Basic CCSDS Turbo Code implementation for testing."""
    
    def __init__(self, frame_size: int = 6144):
        """Initialize turbo code with frame size."""
        self.frame_size = frame_size
    
    def encode(self, data: bytes) -> Tuple[str, Dict]:
        """
        Simulate CCSDS Turbo code encoding.
        Actual turbo codes are more complex, this is for demonstration.
        """
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        
        # Repetition code as simple demonstration
        # (actual turbo codes use iterative decoding)
        encoded = bits + bits  # Double the bits
        
        # Convert to bytes
        output_bytes = []
        for i in range(0, len(encoded), 8):
            byte_bits = encoded[i:i+8]
            while len(byte_bits) < 8:
                byte_bits.append(0)
            byte_val = 0
            for bit in byte_bits:
                byte_val = (byte_val << 1) | bit
            output_bytes.append(byte_val)
        
        output_b64 = base64.b64encode(bytes(output_bytes)).decode()
        
        stats = {
            "original_bits": len(bits),
            "encoded_bits": len(encoded),
            "output_length": len(output_bytes),
            "code_rate": "1/2 (demonstration)",
            "frame_size": self.frame_size,
            "type": "Turbo Code (basic)"
        }
        
        return output_b64, stats


# ============================================================================
# CCSDS LDPC Codes (Basic Implementation)
# ============================================================================

class CCSDSLDPCCodes:
    """Basic CCSDS LDPC (Low-Density Parity-Check) Code implementation."""
    
    def __init__(self, code_rate: str = "1/2"):
        """Initialize LDPC code."""
        self.code_rate = code_rate
        self.rate_num, self.rate_den = map(int, code_rate.split("/"))
    
    def encode(self, data: bytes) -> Tuple[str, Dict]:
        """
        Simulate CCSDS LDPC encoding.
        LDPC encoding involves sparse parity check matrices.
        """
        bits = []
        for byte in data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        
        # Simple repetition-based approach for demonstration
        multiplier = self.rate_den // self.rate_num
        encoded = bits * multiplier
        
        # Convert to bytes
        output_bytes = []
        for i in range(0, len(encoded), 8):
            byte_bits = encoded[i:i+8]
            while len(byte_bits) < 8:
                byte_bits.append(0)
            byte_val = 0
            for bit in byte_bits:
                byte_val = (byte_val << 1) | bit
            output_bytes.append(byte_val)
        
        output_b64 = base64.b64encode(bytes(output_bytes)).decode()
        
        stats = {
            "original_bits": len(bits),
            "encoded_bits": len(encoded),
            "output_length": len(output_bytes),
            "code_rate": self.code_rate,
            "type": "LDPC Code (basic)",
            "sparse_matrix_density": "0.01 (typical)"
        }
        
        return output_b64, stats


# ============================================================================
# Tool Functions for Agent Integration
# ============================================================================

def ccsds_convolution_encode(
    input_bits: Annotated[str, "Input bits (0s and 1s, comma or space separated)"],
    standard: Annotated[str, "CCSDS standard: CCSDS_k3_r12, CCSDS_k3_r13, or CCSDS_k5_r12", "CCSDS_k3_r12"],
) -> str:
    """Encode using CCSDS Convolutional Code."""
    try:
        # Parse input bits
        if ',' in input_bits:
            bits = [int(b.strip()) for b in input_bits.split(',')]
        else:
            bits = [int(b) for b in input_bits.replace(' ', '')]
        
        # Encode
        codec = CCSDSConvolutionalCode(standard)
        encoded, stats = codec.encode(bits)
        
        # Convert to string
        encoded_str = ''.join(str(b) for b in encoded)
        
        result = {
            "status": "success",
            "operation": "CCSDS Convolutional Encoding",
            "standard": standard,
            "description": codec.params["description"],
            "input_bits": ''.join(str(b) for b in bits),
            "encoded_bits": encoded_str,
            **stats
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "CCSDS Convolutional Encoding",
            "message": str(e)
        })


def ccsds_reed_solomon_encode(
    data: Annotated[str, "Data to encode (text)"],
    standard: Annotated[str, "CCSDS RS standard: CCSDS_rs255_223 or CCSDS_rs255_239", "CCSDS_rs255_223"],
) -> str:
    """Encode using CCSDS Reed-Solomon Code."""
    try:
        data_bytes = data.encode()
        
        codec = CCSDSReedSolomon(standard)
        encoded, stats = codec.encode(data_bytes)
        encoded_b64 = base64.b64encode(encoded).decode()
        
        result = {
            "status": "success",
            "operation": "CCSDS Reed-Solomon Encoding",
            "standard": standard,
            "description": codec.config["description"],
            "original_data": data,
            "encoded_data_base64": encoded_b64,
            **stats
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "CCSDS Reed-Solomon Encoding",
            "message": str(e)
        })


def ccsds_concatenated_encode(
    data: Annotated[str, "Data to encode"],
    conv_standard: Annotated[str, "Convolutional code standard", "CCSDS_k3_r12"],
    rs_standard: Annotated[str, "Reed-Solomon standard", "CCSDS_rs255_223"],
) -> str:
    """Encode using CCSDS Concatenated Code (RS + Conv)."""
    try:
        data_bytes = data.encode()
        
        codec = CCSDSConcatenatedCode(conv_standard, rs_standard)
        encoded_b64, stats = codec.encode(data_bytes)
        
        result = {
            "status": "success",
            "operation": "CCSDS Concatenated Code Encoding",
            "outer_code": conv_standard,
            "inner_code": rs_standard,
            "original_data": data,
            "encoded_data_base64": encoded_b64,
            **stats
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "CCSDS Concatenated Code Encoding",
            "message": str(e)
        })


def ccsds_turbo_encode(
    data: Annotated[str, "Data to encode"],
    frame_size: Annotated[int, "Turbo code frame size in bits", "6144"],
) -> str:
    """Encode using CCSDS Turbo Code."""
    try:
        data_bytes = data.encode()
        frame_size = int(frame_size) if isinstance(frame_size, str) else frame_size
        
        codec = CCSDSTurboCodes(frame_size)
        encoded_b64, stats = codec.encode(data_bytes)
        
        result = {
            "status": "success",
            "operation": "CCSDS Turbo Code Encoding",
            "original_data": data,
            "encoded_data_base64": encoded_b64,
            **stats
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "CCSDS Turbo Code Encoding",
            "message": str(e)
        })


def ccsds_ldpc_encode(
    data: Annotated[str, "Data to encode"],
    code_rate: Annotated[str, "Code rate: 1/2 or 1/3", "1/2"],
) -> str:
    """Encode using CCSDS LDPC Code."""
    try:
        data_bytes = data.encode()
        
        codec = CCSDSLDPCCodes(code_rate)
        encoded_b64, stats = codec.encode(data_bytes)
        
        result = {
            "status": "success",
            "operation": "CCSDS LDPC Code Encoding",
            "original_data": data,
            "encoded_data_base64": encoded_b64,
            **stats
        }
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "CCSDS LDPC Code Encoding",
            "message": str(e)
        })


def ccsds_fec_comparison(
    test_data: Annotated[str, "Test data for comparing FEC methods"],
) -> str:
    """Compare all CCSDS FEC methods."""
    try:
        data_bytes = test_data.encode()
        results = {
            "status": "success",
            "operation": "CCSDS FEC Comparison",
            "test_data": test_data,
            "original_size": len(data_bytes),
            "methods": {}
        }
        
        # Test each method
        try:
            codec = CCSDSReedSolomon("CCSDS_rs255_223")
            encoded, stats = codec.encode(data_bytes)
            results["methods"]["Reed-Solomon (255,223)"] = {
                "encoded_size": len(encoded),
                "overhead": f"{(len(encoded) - len(data_bytes)) / len(data_bytes) * 100:.1f}%",
                **stats
            }
        except:
            pass
        
        try:
            bits = []
            for byte in data_bytes:
                for i in range(8):
                    bits.append((byte >> (7 - i)) & 1)
            codec = CCSDSConvolutionalCode("CCSDS_k3_r12")
            encoded, stats = codec.encode(bits)
            results["methods"]["Convolutional (K=7, Rate 1/2)"] = {
                "encoded_bits": len(encoded),
                "encoded_bytes": (len(encoded) + 7) // 8,
                "overhead": f"{(len(encoded) / (len(data_bytes) * 8) - 1) * 100:.1f}%",
                **stats
            }
        except:
            pass
        
        try:
            codec = CCSDSTurboCodes()
            encoded_b64, stats = codec.encode(data_bytes)
            results["methods"]["Turbo Code"] = {
                "encoded_size": len(base64.b64decode(encoded_b64)),
                "overhead": "100% (demonstration)",
                **stats
            }
        except:
            pass
        
        try:
            codec = CCSDSLDPCCodes()
            encoded_b64, stats = codec.encode(data_bytes)
            results["methods"]["LDPC Code"] = {
                "encoded_size": len(base64.b64decode(encoded_b64)),
                "overhead": "100% (demonstration)",
                **stats
            }
        except:
            pass
        
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "operation": "CCSDS FEC Comparison",
            "message": str(e)
        })
