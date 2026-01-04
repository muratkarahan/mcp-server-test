"""
Unit Tests for Reed-Solomon Encoding

Tests Reed-Solomon error correction code encoding and decoding.
Verifies error correction capability and edge cases.
"""

import unittest
import json
import base64
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.encoding_tools import reed_solomon_encode, reed_solomon_decode


class TestReedSolomonEncoding(unittest.TestCase):
    """Test Reed-Solomon encoding"""
    
    def test_encode_basic(self):
        """Test basic RS encoding"""
        data = "Hello World"
        nsym = 10
        
        result_json = reed_solomon_encode(data, nsym)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["original_data"], data)
        self.assertEqual(result["error_correction_symbols"], nsym)
        self.assertIn("encoded_data_base64", result)
    
    def test_encode_with_different_nsym(self):
        """Test encoding with different error correction symbol counts"""
        data = "Test"
        
        for nsym in [5, 10, 20, 32]:
            result_json = reed_solomon_encode(data, nsym)
            result = json.loads(result_json)
            
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["error_correction_symbols"], nsym)
    
    def test_encode_empty_string(self):
        """Test encoding empty string"""
        data = ""
        nsym = 10
        
        result_json = reed_solomon_encode(data, nsym)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
    
    def test_encode_single_byte(self):
        """Test encoding single byte"""
        data = "A"
        nsym = 5
        
        result_json = reed_solomon_encode(data, nsym)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["original_length"], 1)
    
    def test_encode_long_data(self):
        """Test encoding long data"""
        data = "A" * 1000
        nsym = 10
        
        result_json = reed_solomon_encode(data, nsym)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["original_length"], 1000)
        # Encoded should be longer due to parity symbols
        self.assertGreater(result["encoded_length"], result["original_length"])
    
    def test_encode_special_characters(self):
        """Test encoding with special characters"""
        data = "!@#$%^&*()\n\t"
        nsym = 10
        
        result_json = reed_solomon_encode(data, nsym)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
    
    def test_encode_returns_base64(self):
        """Test that encoding returns base64 data"""
        data = "Test"
        nsym = 10
        
        result_json = reed_solomon_encode(data, nsym)
        result = json.loads(result_json)
        
        encoded_b64 = result["encoded_data_base64"]
        # Should be valid base64
        decoded = base64.b64decode(encoded_b64)
        self.assertGreater(len(decoded), 0)
    
    def test_encode_returns_json(self):
        """Test that encoding returns valid JSON"""
        data = "Test"
        nsym = 10
        
        result_json = reed_solomon_encode(data, nsym)
        result = json.loads(result_json)
        
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)
        self.assertIn("operation", result)


class TestReedSolomonDecoding(unittest.TestCase):
    """Test Reed-Solomon decoding"""
    
    def test_decode_basic(self):
        """Test basic RS decoding"""
        data = "Hello World"
        nsym = 10
        
        # Encode
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        encoded_b64 = encoded_result["encoded_data_base64"]
        
        # Decode
        decoded_json = reed_solomon_decode(encoded_b64, nsym)
        decoded_result = json.loads(decoded_json)
        
        self.assertEqual(decoded_result["status"], "success")
        self.assertEqual(decoded_result["decoded_data"], data)
        self.assertEqual(decoded_result["errors_corrected"], 0)
    
    def test_decode_empty_string(self):
        """Test decoding empty string"""
        data = ""
        nsym = 10
        
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        encoded_b64 = encoded_result["encoded_data_base64"]
        
        decoded_json = reed_solomon_decode(encoded_b64, nsym)
        decoded_result = json.loads(decoded_json)
        
        self.assertEqual(decoded_result["status"], "success")
        self.assertEqual(decoded_result["decoded_data"], data)
    
    def test_decode_with_errors(self):
        """Test decoding with introduced errors"""
        data = "Test Message"
        nsym = 10
        
        # Encode
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        encoded_b64 = encoded_result["encoded_data_base64"]
        
        # Corrupt some bytes
        encoded_bytes = bytearray(base64.b64decode(encoded_b64))
        # Introduce a few errors (up to nsym/2 can be corrected)
        encoded_bytes[0] ^= 0xFF  # Flip bits in first byte
        encoded_bytes[5] ^= 0xFF
        corrupted_b64 = base64.b64encode(bytes(encoded_bytes)).decode()
        
        # Decode
        decoded_json = reed_solomon_decode(corrupted_b64, nsym)
        decoded_result = json.loads(decoded_json)
        
        self.assertEqual(decoded_result["status"], "success")
        self.assertEqual(decoded_result["decoded_data"], data)
        # Should have detected and corrected errors
        self.assertGreater(decoded_result["errors_corrected"], 0)
    
    def test_decode_too_many_errors(self):
        """Test decoding with too many errors"""
        data = "Test"
        nsym = 10
        
        # Encode
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        encoded_b64 = encoded_result["encoded_data_base64"]
        
        # Corrupt many bytes (more than nsym/2)
        encoded_bytes = bytearray(base64.b64decode(encoded_b64))
        for i in range(min(10, len(encoded_bytes))):
            encoded_bytes[i] = 0xFF
        corrupted_b64 = base64.b64encode(bytes(encoded_bytes)).decode()
        
        # Try to decode
        decoded_json = reed_solomon_decode(corrupted_b64, nsym)
        decoded_result = json.loads(decoded_json)
        
        # Should have error status
        self.assertEqual(decoded_result["status"], "error")
    
    def test_decode_invalid_base64(self):
        """Test decoding invalid base64"""
        invalid_b64 = "not-valid-base64!!!"
        nsym = 10
        
        decoded_json = reed_solomon_decode(invalid_b64, nsym)
        decoded_result = json.loads(decoded_json)
        
        self.assertEqual(decoded_result["status"], "error")
    
    def test_decode_returns_json(self):
        """Test that decoding returns valid JSON"""
        data = "Test"
        nsym = 10
        
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        encoded_b64 = encoded_result["encoded_data_base64"]
        
        decoded_json = reed_solomon_decode(encoded_b64, nsym)
        result = json.loads(decoded_json)
        
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)


class TestReedSolomonRoundTrip(unittest.TestCase):
    """Test RS encoding/decoding round trips"""
    
    def test_roundtrip_basic(self):
        """Test encode then decode returns original"""
        data = "Test Message"
        nsym = 10
        
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        
        decoded_json = reed_solomon_decode(encoded_result["encoded_data_base64"], nsym)
        decoded_result = json.loads(decoded_json)
        
        self.assertEqual(decoded_result["decoded_data"], data)
    
    def test_roundtrip_various_nsym(self):
        """Test round trip with various nsym values"""
        data = "Test"
        
        for nsym in [5, 10, 20]:
            encoded_json = reed_solomon_encode(data, nsym)
            encoded_result = json.loads(encoded_json)
            
            decoded_json = reed_solomon_decode(encoded_result["encoded_data_base64"], nsym)
            decoded_result = json.loads(decoded_json)
            
            self.assertEqual(decoded_result["decoded_data"], data,
                           f"Failed for nsym={nsym}")
    
    def test_roundtrip_various_lengths(self):
        """Test round trip with various data lengths"""
        nsym = 10
        
        for length in [1, 10, 50, 100]:
            data = "A" * length
            
            encoded_json = reed_solomon_encode(data, nsym)
            encoded_result = json.loads(encoded_json)
            
            decoded_json = reed_solomon_decode(encoded_result["encoded_data_base64"], nsym)
            decoded_result = json.loads(decoded_json)
            
            self.assertEqual(decoded_result["decoded_data"], data,
                           f"Failed for length={length}")
    
    def test_roundtrip_with_single_error(self):
        """Test round trip with single introduced error"""
        data = "Test Message for Error Correction"
        nsym = 10
        
        # Encode
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        encoded_b64 = encoded_result["encoded_data_base64"]
        
        # Introduce single error
        encoded_bytes = bytearray(base64.b64decode(encoded_b64))
        encoded_bytes[0] ^= 0xFF
        corrupted_b64 = base64.b64encode(bytes(encoded_bytes)).decode()
        
        # Decode
        decoded_json = reed_solomon_decode(corrupted_b64, nsym)
        decoded_result = json.loads(decoded_json)
        
        self.assertEqual(decoded_result["status"], "success")
        self.assertEqual(decoded_result["decoded_data"], data)


class TestReedSolomonErrorCorrection(unittest.TestCase):
    """Test error correction capability"""
    
    def test_error_positions_returned(self):
        """Test that error positions are returned"""
        data = "Test"
        nsym = 10
        
        # Encode
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        encoded_b64 = encoded_result["encoded_data_base64"]
        
        # Introduce error
        encoded_bytes = bytearray(base64.b64decode(encoded_b64))
        encoded_bytes[5] ^= 0xFF
        corrupted_b64 = base64.b64encode(bytes(encoded_bytes)).decode()
        
        # Decode
        decoded_json = reed_solomon_decode(corrupted_b64, nsym)
        decoded_result = json.loads(decoded_json)
        
        self.assertEqual(decoded_result["status"], "success")
        self.assertIsInstance(decoded_result["error_positions"], list)
    
    def test_correction_capability_nsym_10(self):
        """Test correction capability with nsym=10"""
        # Can correct up to nsym/2 errors
        data = "Test Data"
        nsym = 10
        max_correctable = nsym // 2
        
        encoded_json = reed_solomon_encode(data, nsym)
        encoded_result = json.loads(encoded_json)
        encoded_b64 = encoded_result["encoded_data_base64"]
        
        # Introduce max correctable errors
        encoded_bytes = bytearray(base64.b64decode(encoded_b64))
        for i in range(max_correctable):
            if i < len(encoded_bytes):
                encoded_bytes[i] ^= 0xFF
        corrupted_b64 = base64.b64encode(bytes(encoded_bytes)).decode()
        
        # Should still decode correctly
        decoded_json = reed_solomon_decode(corrupted_b64, nsym)
        decoded_result = json.loads(decoded_json)
        
        self.assertEqual(decoded_result["status"], "success")
        self.assertEqual(decoded_result["decoded_data"], data)


if __name__ == "__main__":
    unittest.main()
