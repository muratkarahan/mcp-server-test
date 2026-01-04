"""
Integration Tests for Encoding Tools

Tests the tool functions that return JSON responses for agent integration.
Verifies that all tools return properly formatted JSON with correct status codes.
"""

import unittest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.encoding_tools import (
    aes_encrypt, aes_decrypt,
    reed_solomon_encode, reed_solomon_decode,
    convolution_encode, convolution_test
)
from tools.ccsds_fec import (
    ccsds_convolution_encode,
    ccsds_reed_solomon_encode,
    ccsds_concatenated_encode,
    ccsds_turbo_encode,
    ccsds_ldpc_encode,
    ccsds_fec_comparison
)


class TestToolJSONResponses(unittest.TestCase):
    """Test that all tools return valid JSON responses"""
    
    def test_aes_encrypt_returns_json(self):
        """Test AES encrypt returns valid JSON"""
        result = aes_encrypt("Test", "key")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_aes_decrypt_returns_json(self):
        """Test AES decrypt returns valid JSON"""
        encrypted = json.loads(aes_encrypt("Test", "key"))
        result = aes_decrypt(encrypted["ciphertext_base64"], "key")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_reed_solomon_encode_returns_json(self):
        """Test RS encode returns valid JSON"""
        result = reed_solomon_encode("Test", 10)
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_reed_solomon_decode_returns_json(self):
        """Test RS decode returns valid JSON"""
        encoded = json.loads(reed_solomon_encode("Test", 10))
        result = reed_solomon_decode(encoded["encoded_data_base64"], 10)
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_convolution_encode_returns_json(self):
        """Test Convolution encode returns valid JSON"""
        result = convolution_encode("10110", "7,5")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_convolution_test_returns_json(self):
        """Test Convolution test returns valid JSON"""
        result = convolution_test("demo")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_ccsds_convolution_encode_returns_json(self):
        """Test CCSDS Conv encode returns valid JSON"""
        result = ccsds_convolution_encode("1, 0, 1", "CCSDS_k3_r12")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_ccsds_reed_solomon_encode_returns_json(self):
        """Test CCSDS RS encode returns valid JSON"""
        result = ccsds_reed_solomon_encode("Test", "CCSDS_rs255_223")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_ccsds_concatenated_encode_returns_json(self):
        """Test CCSDS concatenated encode returns valid JSON"""
        result = ccsds_concatenated_encode("Test")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_ccsds_turbo_encode_returns_json(self):
        """Test CCSDS turbo encode returns valid JSON"""
        result = ccsds_turbo_encode("Test")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_ccsds_ldpc_encode_returns_json(self):
        """Test CCSDS LDPC encode returns valid JSON"""
        result = ccsds_ldpc_encode("Test", "1/2")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)
    
    def test_ccsds_fec_comparison_returns_json(self):
        """Test CCSDS FEC comparison returns valid JSON"""
        result = ccsds_fec_comparison("Test")
        data = json.loads(result)
        
        self.assertIn("status", data)
        self.assertIn("operation", data)


class TestSuccessStatuses(unittest.TestCase):
    """Test that successful operations return success status"""
    
    def test_aes_encrypt_success(self):
        """Test AES encrypt returns success"""
        result = json.loads(aes_encrypt("Test", "key"))
        self.assertEqual(result["status"], "success")
    
    def test_aes_decrypt_success(self):
        """Test AES decrypt returns success"""
        encrypted = json.loads(aes_encrypt("Test", "key"))
        result = json.loads(aes_decrypt(encrypted["ciphertext_base64"], "key"))
        self.assertEqual(result["status"], "success")
    
    def test_reed_solomon_success(self):
        """Test RS returns success"""
        result = json.loads(reed_solomon_encode("Test", 10))
        self.assertEqual(result["status"], "success")
    
    def test_convolution_success(self):
        """Test Convolution returns success"""
        result = json.loads(convolution_encode("10110", "7,5"))
        self.assertEqual(result["status"], "success")
    
    def test_all_ccsds_tools_success(self):
        """Test all CCSDS tools return success"""
        tools_results = [
            ccsds_convolution_encode("1, 0, 1", "CCSDS_k3_r12"),
            ccsds_reed_solomon_encode("Test", "CCSDS_rs255_223"),
            ccsds_concatenated_encode("Test"),
            ccsds_turbo_encode("Test"),
            ccsds_ldpc_encode("Test", "1/2"),
            ccsds_fec_comparison("Test"),
        ]
        
        for result_json in tools_results:
            result = json.loads(result_json)
            self.assertEqual(result["status"], "success")


class TestErrorHandling(unittest.TestCase):
    """Test error handling and error messages"""
    
    def test_invalid_base64_returns_error(self):
        """Test invalid base64 returns error status"""
        result = json.loads(aes_decrypt("invalid!!!", "key"))
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)
    
    def test_reed_solomon_error_message(self):
        """Test RS error has message field"""
        result = json.loads(reed_solomon_decode("invalid", 10))
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)
    
    def test_error_has_operation_field(self):
        """Test error responses include operation field"""
        result = json.loads(aes_decrypt("invalid", "key"))
        self.assertIn("operation", result)


class TestToolParameterValidation(unittest.TestCase):
    """Test parameter validation and type handling"""
    
    def test_reed_solomon_nsym_string(self):
        """Test RS accepts nsym as string"""
        result = json.loads(reed_solomon_encode("Test", "10"))
        self.assertEqual(result["status"], "success")
    
    def test_reed_solomon_nsym_integer(self):
        """Test RS accepts nsym as integer"""
        result = json.loads(reed_solomon_encode("Test", 10))
        self.assertEqual(result["status"], "success")
    
    def test_ccsds_turbo_frame_size_string(self):
        """Test Turbo accepts frame_size as string"""
        result = json.loads(ccsds_turbo_encode("Test", "6144"))
        self.assertEqual(result["status"], "success")
    
    def test_ccsds_turbo_frame_size_integer(self):
        """Test Turbo accepts frame_size as integer"""
        result = json.loads(ccsds_turbo_encode("Test", 6144))
        self.assertEqual(result["status"], "success")


class TestDataPreservation(unittest.TestCase):
    """Test that data is properly preserved in responses"""
    
    def test_aes_encrypt_preserves_plaintext(self):
        """Test AES encrypt response contains original plaintext"""
        plaintext = "Original Message"
        result = json.loads(aes_encrypt(plaintext, "key"))
        
        self.assertEqual(result["plaintext"], plaintext)
    
    def test_aes_decrypt_preserves_ciphertext(self):
        """Test AES decrypt response contains ciphertext"""
        encrypted = json.loads(aes_encrypt("Test", "key"))
        result = json.loads(aes_decrypt(encrypted["ciphertext_base64"], "key"))
        
        self.assertEqual(result["ciphertext_base64"], encrypted["ciphertext_base64"])
    
    def test_reed_solomon_encode_preserves_data(self):
        """Test RS encode preserves original data"""
        data = "Test Data"
        result = json.loads(reed_solomon_encode(data, 10))
        
        self.assertEqual(result["original_data"], data)
    
    def test_convolution_encode_preserves_input(self):
        """Test Convolution encode preserves input"""
        input_bits = "10110"
        result = json.loads(convolution_encode(input_bits, "7,5"))
        
        # Input bits should be normalized in output
        self.assertEqual(result["input_bits"], "10110")


class TestStatisticsProvided(unittest.TestCase):
    """Test that operations provide statistics"""
    
    def test_aes_encrypt_provides_sizes(self):
        """Test AES encrypt provides size information"""
        result = json.loads(aes_encrypt("Test", "key"))
        
        self.assertIn("plaintext_length", result)
        self.assertIn("ciphertext_length", result)
    
    def test_reed_solomon_provides_stats(self):
        """Test RS provides encoding statistics"""
        result = json.loads(reed_solomon_encode("Test", 10))
        
        self.assertIn("original_length", result)
        self.assertIn("encoded_length", result)
        self.assertIn("error_correction_symbols", result)
    
    def test_convolution_provides_rate(self):
        """Test Convolution provides code rate"""
        result = json.loads(convolution_encode("10110", "7,5"))
        
        self.assertIn("code_rate", result)
        self.assertIn("expansion_ratio", result)
    
    def test_ccsds_tools_provide_stats(self):
        """Test CCSDS tools provide statistics"""
        result = json.loads(ccsds_concatenated_encode("Test"))
        
        self.assertIn("original_data_length", result)
        self.assertIn("overall_code_rate", result)


if __name__ == "__main__":
    unittest.main()
