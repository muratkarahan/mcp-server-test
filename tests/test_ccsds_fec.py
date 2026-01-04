"""
Unit Tests for CCSDS FEC Standards

Tests NASA CCSDS Forward Error Correction implementations:
- Convolutional codes (K=7, K=5)
- Reed-Solomon codes (255,223), (255,239)
- Concatenated codes
- Turbo codes
- LDPC codes
"""

import unittest
import json
import base64
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.ccsds_fec import (
    CCSDSConvolutionalCode,
    CCSDSReedSolomon,
    CCSDSConcatenatedCode,
    CCSDSTurboCodes,
    CCSDSLDPCCodes,
    ccsds_convolution_encode,
    ccsds_reed_solomon_encode,
    ccsds_concatenated_encode,
    ccsds_turbo_encode,
    ccsds_ldpc_encode,
    ccsds_fec_comparison
)


class TestCCSDSConvolutionalCode(unittest.TestCase):
    """Test CCSDS Convolutional Code"""
    
    def test_ccsds_k7_r12_encode(self):
        """Test CCSDS K=7, Rate 1/2 encoding"""
        codec = CCSDSConvolutionalCode("CCSDS_k3_r12")
        input_bits = [1, 0, 1, 1, 0]
        
        encoded, stats = codec.encode(input_bits)
        
        self.assertEqual(stats["constraint_length"], 7)
        self.assertEqual(stats["code_rate"], "1/2")
        # Rate 1/2 produces 2x bits
        self.assertEqual(len(encoded), len(input_bits) * 2)
    
    def test_ccsds_k7_r13_encode(self):
        """Test CCSDS K=7, Rate 1/3 encoding"""
        codec = CCSDSConvolutionalCode("CCSDS_k3_r13")
        input_bits = [1, 0, 1]
        
        encoded, stats = codec.encode(input_bits)
        
        self.assertEqual(stats["constraint_length"], 7)
        self.assertEqual(stats["code_rate"], "1/3")
        # Rate 1/3 produces 3x bits
        self.assertEqual(len(encoded), len(input_bits) * 3)
    
    def test_ccsds_k5_r12_encode(self):
        """Test CCSDS K=5, Rate 1/2 encoding"""
        codec = CCSDSConvolutionalCode("CCSDS_k5_r12")
        input_bits = [1, 0, 1]
        
        encoded, stats = codec.encode(input_bits)
        
        self.assertEqual(stats["constraint_length"], 5)
        self.assertEqual(stats["code_rate"], "1/2")
    
    def test_invalid_standard(self):
        """Test invalid standard raises error"""
        with self.assertRaises(ValueError):
            CCSDSConvolutionalCode("INVALID_STANDARD")
    
    def test_ccsds_convolution_encode_tool(self):
        """Test CCSDS convolution encode tool function"""
        input_bits = "1, 0, 1, 1"
        standard = "CCSDS_k3_r12"
        
        result_json = ccsds_convolution_encode(input_bits, standard)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["standard"], standard)
        self.assertIn("encoded_bits", result)


class TestCCSDSReedSolomon(unittest.TestCase):
    """Test CCSDS Reed-Solomon Code"""
    
    def test_ccsds_rs255_223_encode(self):
        """Test CCSDS (255,223) encoding"""
        codec = CCSDSReedSolomon("CCSDS_rs255_223")
        data = b"Test Data"
        
        encoded, stats = codec.encode(data)
        
        self.assertEqual(stats["parity_symbols"], 32)
        self.assertEqual(stats["error_correction_capability"], 16)
        self.assertEqual(stats["code_rate"], "223/255")
        self.assertGreater(len(encoded), len(data))
    
    def test_ccsds_rs255_239_encode(self):
        """Test CCSDS (255,239) encoding"""
        codec = CCSDSReedSolomon("CCSDS_rs255_239")
        data = b"Test Data"
        
        encoded, stats = codec.encode(data)
        
        self.assertEqual(stats["parity_symbols"], 16)
        self.assertEqual(stats["error_correction_capability"], 8)
        self.assertEqual(stats["code_rate"], "239/255")
    
    def test_ccsds_rs_decode(self):
        """Test CCSDS RS decoding"""
        codec = CCSDSReedSolomon("CCSDS_rs255_223")
        original = b"Space Data"
        
        encoded, _ = codec.encode(original)
        decoded, stats = codec.decode(encoded)
        
        self.assertEqual(decoded, original)
        self.assertEqual(stats["errors_corrected"], 0)
    
    def test_ccsds_rs_roundtrip(self):
        """Test CCSDS RS encode/decode roundtrip"""
        for standard in ["CCSDS_rs255_223", "CCSDS_rs255_239"]:
            codec = CCSDSReedSolomon(standard)
            original = b"Test Message"
            
            encoded, _ = codec.encode(original)
            decoded, _ = codec.decode(encoded)
            
            self.assertEqual(decoded, original,
                           f"Failed for {standard}")
    
    def test_ccsds_reed_solomon_encode_tool(self):
        """Test CCSDS RS encode tool function"""
        data = "Test Data"
        standard = "CCSDS_rs255_223"
        
        result_json = ccsds_reed_solomon_encode(data, standard)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["standard"], standard)
        self.assertIn("encoded_data_base64", result)


class TestCCSDSConcatenatedCode(unittest.TestCase):
    """Test CCSDS Concatenated Code"""
    
    def test_concatenated_encode(self):
        """Test concatenated encoding"""
        codec = CCSDSConcatenatedCode()
        data = b"Test Data"
        
        encoded_b64, stats = codec.encode(data)
        
        self.assertEqual(stats["original_data_length"], len(data))
        self.assertIn("output_length", stats)
        self.assertGreater(stats["output_length"], len(data))
    
    def test_concatenated_with_different_configs(self):
        """Test concatenated with different configurations"""
        data = b"Test"
        
        configs = [
            ("CCSDS_k3_r12", "CCSDS_rs255_223"),
            ("CCSDS_k3_r13", "CCSDS_rs255_223"),
            ("CCSDS_k3_r12", "CCSDS_rs255_239"),
        ]
        
        for conv_std, rs_std in configs:
            codec = CCSDSConcatenatedCode(conv_std, rs_std)
            encoded_b64, stats = codec.encode(data)
            
            self.assertIn("overall_code_rate", stats)
            self.assertGreater(stats["output_length"], 0)
    
    def test_ccsds_concatenated_encode_tool(self):
        """Test CCSDS concatenated encode tool function"""
        data = "Test Data"
        
        result_json = ccsds_concatenated_encode(data)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("encoded_data_base64", result)
        self.assertIn("outer_code", result)
        self.assertIn("inner_code", result)


class TestCCSDSTurboCodes(unittest.TestCase):
    """Test CCSDS Turbo Code"""
    
    def test_turbo_encode(self):
        """Test turbo code encoding"""
        codec = CCSDSTurboCodes()
        data = b"Test Data"
        
        encoded_b64, stats = codec.encode(data)
        
        self.assertEqual(stats["code_rate"], "1/2 (demonstration)")
        self.assertIn("output_length", stats)
        decoded = base64.b64decode(encoded_b64)
        self.assertGreater(len(decoded), 0)
    
    def test_turbo_with_custom_frame_size(self):
        """Test turbo with custom frame size"""
        frame_size = 8192
        codec = CCSDSTurboCodes(frame_size)
        data = b"Test"
        
        encoded_b64, stats = codec.encode(data)
        
        self.assertEqual(stats["frame_size"], frame_size)
    
    def test_ccsds_turbo_encode_tool(self):
        """Test CCSDS turbo encode tool function"""
        data = "Test Data"
        
        result_json = ccsds_turbo_encode(data)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("encoded_data_base64", result)


class TestCCSDSLDPCCodes(unittest.TestCase):
    """Test CCSDS LDPC Code"""
    
    def test_ldpc_rate_1_2(self):
        """Test LDPC Rate 1/2"""
        codec = CCSDSLDPCCodes("1/2")
        data = b"Test Data"
        
        encoded_b64, stats = codec.encode(data)
        
        self.assertEqual(stats["code_rate"], "1/2")
        decoded = base64.b64decode(encoded_b64)
        self.assertGreater(len(decoded), 0)
    
    def test_ldpc_rate_1_3(self):
        """Test LDPC Rate 1/3"""
        codec = CCSDSLDPCCodes("1/3")
        data = b"Test Data"
        
        encoded_b64, stats = codec.encode(data)
        
        self.assertEqual(stats["code_rate"], "1/3")
    
    def test_ccsds_ldpc_encode_tool(self):
        """Test CCSDS LDPC encode tool function"""
        data = "Test Data"
        
        result_json = ccsds_ldpc_encode(data, "1/2")
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("encoded_data_base64", result)


class TestCCSDSFECComparison(unittest.TestCase):
    """Test CCSDS FEC Comparison tool"""
    
    def test_fec_comparison(self):
        """Test FEC comparison"""
        test_data = "Test Message"
        
        result_json = ccsds_fec_comparison(test_data)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("methods", result)
        self.assertGreater(len(result["methods"]), 0)
    
    def test_comparison_contains_all_methods(self):
        """Test that comparison includes all methods"""
        result_json = ccsds_fec_comparison("Test")
        result = json.loads(result_json)
        
        methods = result["methods"]
        # Should have results for various methods
        self.assertGreater(len(methods), 3)
    
    def test_comparison_returns_statistics(self):
        """Test that comparison returns statistics"""
        result_json = ccsds_fec_comparison("Test")
        result = json.loads(result_json)
        
        for method_name, method_data in result["methods"].items():
            self.assertIn("overhead", method_data)


class TestCCSDSStandardGeneratorPolynomials(unittest.TestCase):
    """Test CCSDS standard generator polynomials"""
    
    def test_ccsds_k7_r12_generators(self):
        """Test CCSDS K=7 Rate 1/2 generators"""
        codec = CCSDSConvolutionalCode("CCSDS_k3_r12")
        
        # NASA standard generators
        self.assertEqual(len(codec.generators), 2)
        self.assertEqual(codec.generators[0], 0o171)  # Octal 171
        self.assertEqual(codec.generators[1], 0o133)  # Octal 133
    
    def test_ccsds_k7_r13_generators(self):
        """Test CCSDS K=7 Rate 1/3 generators"""
        codec = CCSDSConvolutionalCode("CCSDS_k3_r13")
        
        self.assertEqual(len(codec.generators), 3)
        self.assertEqual(codec.generators[0], 0o171)
        self.assertEqual(codec.generators[1], 0o133)
        self.assertEqual(codec.generators[2], 0o145)
    
    def test_ccsds_k5_r12_generators(self):
        """Test CCSDS K=5 Rate 1/2 generators"""
        codec = CCSDSConvolutionalCode("CCSDS_k5_r12")
        
        self.assertEqual(len(codec.generators), 2)
        self.assertEqual(codec.generators[0], 0o31)  # Octal 31
        self.assertEqual(codec.generators[1], 0o27)  # Octal 27


if __name__ == "__main__":
    unittest.main()
