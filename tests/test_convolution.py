"""
Unit Tests for Convolution Encoding

Tests convolution encoding with various generator polynomials.
Verifies code rates and encoding correctness.
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.encoding_tools import convolution_encode, convolution_test


class TestConvolutionEncoding(unittest.TestCase):
    """Test Convolution encoding"""
    
    def test_encode_basic(self):
        """Test basic convolution encoding"""
        input_bits = "10110"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["input_length"], 5)
        self.assertIn("encoded_bits", result)
    
    def test_encode_comma_separated_input(self):
        """Test encoding with comma-separated input"""
        input_bits = "1, 0, 1, 1, 0"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["input_length"], 5)
    
    def test_encode_space_separated_input(self):
        """Test encoding with space-separated input"""
        input_bits = "1 0 1 1 0"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
    
    def test_encode_continuous_input(self):
        """Test encoding with continuous input"""
        input_bits = "101101"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["input_length"], 6)
    
    def test_encode_rate_1_2(self):
        """Test rate 1/2 encoding (2 generator polynomials)"""
        input_bits = "10110"
        gen_poly = "7,5"  # Two polynomials
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code_rate"], "1/2")
        # Output should be 2x input for rate 1/2
        self.assertEqual(result["encoded_length"], result["input_length"] * 2)
    
    def test_encode_rate_1_3(self):
        """Test rate 1/3 encoding (3 generator polynomials)"""
        input_bits = "10110"
        gen_poly = "7,5,3"  # Three polynomials
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code_rate"], "1/3")
        # Output should be 3x input for rate 1/3
        self.assertEqual(result["encoded_length"], result["input_length"] * 3)
    
    def test_encode_single_bit(self):
        """Test encoding single bit"""
        input_bits = "1"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["input_length"], 1)
    
    def test_encode_all_zeros(self):
        """Test encoding all zeros"""
        input_bits = "00000"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        # Should produce all zeros
        self.assertEqual(result["encoded_bits"], "0" * (result["input_length"] * 2))
    
    def test_encode_all_ones(self):
        """Test encoding all ones"""
        input_bits = "11111"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertGreater(len(result["encoded_bits"]), 0)
    
    def test_encode_long_sequence(self):
        """Test encoding long bit sequence"""
        input_bits = "10" * 100  # 200 bits
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["input_length"], 200)
    
    def test_encode_returns_binary_string(self):
        """Test that output is binary string"""
        input_bits = "10110"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        encoded = result["encoded_bits"]
        # Should only contain 0 and 1
        self.assertTrue(all(c in '01' for c in encoded))
    
    def test_encode_returns_json(self):
        """Test that encoding returns valid JSON"""
        input_bits = "10110"
        gen_poly = "7,5"
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("code_rate", result)
    
    def test_encode_expansion_ratio(self):
        """Test expansion ratio calculation"""
        input_bits = "10110"
        gen_poly = "7,5"  # Rate 1/2
        
        result_json = convolution_encode(input_bits, gen_poly)
        result = json.loads(result_json)
        
        # For rate 1/2, expansion should be 2
        self.assertEqual(result["expansion_ratio"], 2.0)


class TestConvolutionTest(unittest.TestCase):
    """Test Convolution test function"""
    
    def test_demo_mode(self):
        """Test demo mode"""
        result_json = convolution_test("demo")
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["test_type"], "demo")
        self.assertIn("tests", result)
        self.assertGreater(len(result["tests"]), 0)
    
    def test_verify_rate_mode(self):
        """Test rate verification mode"""
        result_json = convolution_test("verify_rate")
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["test_type"], "verify_rate")
        self.assertIn("tests", result)
    
    def test_performance_mode(self):
        """Test performance mode"""
        result_json = convolution_test("performance")
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["test_type"], "performance")
        self.assertIn("tests", result)
    
    def test_returns_json(self):
        """Test that function returns valid JSON"""
        result_json = convolution_test("demo")
        result = json.loads(result_json)
        
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("operation", result)


class TestConvolutionGeneratorPolynomials(unittest.TestCase):
    """Test different generator polynomials"""
    
    def test_octal_polynomials(self):
        """Test octal format polynomials"""
        input_bits = "10110"
        
        # NASA standard polynomials (octal)
        polynomials = [
            "7,5",      # (7,5) octal = (111,101) binary
            "171,133",  # (171,133) octal = CCSDS K=7
            "31,27",    # (31,27) octal = Simpler
        ]
        
        for poly in polynomials:
            result_json = convolution_encode(input_bits, poly)
            result = json.loads(result_json)
            
            self.assertEqual(result["status"], "success",
                           f"Failed for polynomial {poly}")
    
    def test_different_polynomials_produce_different_output(self):
        """Test that different polynomials produce different outputs"""
        input_bits = "10110"
        
        result1_json = convolution_encode(input_bits, "7,5")
        result1 = json.loads(result1_json)
        
        result2_json = convolution_encode(input_bits, "7,3")
        result2 = json.loads(result2_json)
        
        # Different polynomials should produce different output
        self.assertNotEqual(
            result1["encoded_bits"],
            result2["encoded_bits"]
        )


if __name__ == "__main__":
    unittest.main()
