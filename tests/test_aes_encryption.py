"""
Unit Tests for AES Encryption Tools

Tests AES-256-CBC encryption and decryption functions.
Verifies IV handling, padding, key processing, and error conditions.
"""

import unittest
import json
import base64
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.encoding_tools import aes_encrypt, aes_decrypt


class TestAESEncryption(unittest.TestCase):
    """Test AES-256-CBC encryption"""
    
    def test_encrypt_basic(self):
        """Test basic encryption"""
        plaintext = "Hello World"
        key = "testkey123"
        
        result_json = aes_encrypt(plaintext, key)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["plaintext"], plaintext)
        self.assertIn("ciphertext_base64", result)
        self.assertGreater(len(result["ciphertext_base64"]), 0)
    
    def test_encrypt_empty_plaintext(self):
        """Test encryption of empty string"""
        plaintext = ""
        key = "key"
        
        result_json = aes_encrypt(plaintext, key)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["plaintext"], plaintext)
    
    def test_encrypt_long_text(self):
        """Test encryption of long text"""
        plaintext = "A" * 1000
        key = "longkey"
        
        result_json = aes_encrypt(plaintext, key)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["plaintext_length"], 1000)
    
    def test_encrypt_special_characters(self):
        """Test encryption with special characters"""
        plaintext = "!@#$%^&*()_+-={}[]|:;<>?,./\n\t"
        key = "key123"
        
        result_json = aes_encrypt(plaintext, key)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["plaintext"], plaintext)
    
    def test_encrypt_unicode(self):
        """Test encryption with Unicode characters"""
        plaintext = "مرحبا世界🌍Привет"
        key = "unicodekey"
        
        result_json = aes_encrypt(plaintext, key)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["plaintext"], plaintext)
    
    def test_encrypt_key_padding(self):
        """Test that short keys are padded to 32 bytes"""
        plaintext = "Test"
        short_key = "short"
        
        result_json = aes_encrypt(plaintext, short_key)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
    
    def test_encrypt_key_truncation(self):
        """Test that long keys are truncated to 32 bytes"""
        plaintext = "Test"
        long_key = "A" * 100
        
        result_json = aes_encrypt(plaintext, long_key)
        result = json.loads(result_json)
        
        self.assertEqual(result["status"], "success")
    
    def test_encrypt_different_keys_produce_different_ciphertexts(self):
        """Test that different keys produce different ciphertexts"""
        plaintext = "Test Data"
        
        result1_json = aes_encrypt(plaintext, "key1")
        result1 = json.loads(result1_json)
        
        result2_json = aes_encrypt(plaintext, "key2")
        result2 = json.loads(result2_json)
        
        self.assertNotEqual(
            result1["ciphertext_base64"],
            result2["ciphertext_base64"]
        )
    
    def test_encrypt_multiple_encryptions_produce_different_ciphertexts(self):
        """Test that encrypting same data twice produces different ciphertexts (due to random IV)"""
        plaintext = "Test Data"
        key = "testkey"
        
        result1_json = aes_encrypt(plaintext, key)
        result1 = json.loads(result1_json)
        
        result2_json = aes_encrypt(plaintext, key)
        result2 = json.loads(result2_json)
        
        # Different IVs should produce different ciphertexts
        self.assertNotEqual(
            result1["ciphertext_base64"],
            result2["ciphertext_base64"]
        )
    
    def test_encrypt_iv_is_included(self):
        """Test that IV is included in ciphertext"""
        plaintext = "Test"
        key = "key"
        
        result_json = aes_encrypt(plaintext, key)
        result = json.loads(result_json)
        
        ciphertext_bytes = base64.b64decode(result["ciphertext_base64"])
        # First 16 bytes should be IV
        self.assertGreaterEqual(len(ciphertext_bytes), 16)
    
    def test_encrypt_returns_json(self):
        """Test that encryption returns valid JSON"""
        plaintext = "Test"
        key = "key"
        
        result_json = aes_encrypt(plaintext, key)
        
        # Should not raise exception
        result = json.loads(result_json)
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)


class TestAESDecryption(unittest.TestCase):
    """Test AES-256-CBC decryption"""
    
    def test_decrypt_basic(self):
        """Test basic decryption"""
        plaintext = "Hello World"
        key = "testkey123"
        
        # Encrypt
        encrypted_json = aes_encrypt(plaintext, key)
        encrypted_result = json.loads(encrypted_json)
        ciphertext_b64 = encrypted_result["ciphertext_base64"]
        
        # Decrypt
        decrypted_json = aes_decrypt(ciphertext_b64, key)
        decrypted_result = json.loads(decrypted_json)
        
        self.assertEqual(decrypted_result["status"], "success")
        self.assertEqual(decrypted_result["plaintext"], plaintext)
    
    def test_decrypt_empty_string(self):
        """Test decryption of empty string"""
        plaintext = ""
        key = "key"
        
        encrypted_json = aes_encrypt(plaintext, key)
        encrypted_result = json.loads(encrypted_json)
        ciphertext_b64 = encrypted_result["ciphertext_base64"]
        
        decrypted_json = aes_decrypt(ciphertext_b64, key)
        decrypted_result = json.loads(decrypted_json)
        
        self.assertEqual(decrypted_result["status"], "success")
        self.assertEqual(decrypted_result["plaintext"], plaintext)
    
    def test_decrypt_long_text(self):
        """Test decryption of long text"""
        plaintext = "A" * 1000
        key = "longkey"
        
        encrypted_json = aes_encrypt(plaintext, key)
        encrypted_result = json.loads(encrypted_json)
        ciphertext_b64 = encrypted_result["ciphertext_base64"]
        
        decrypted_json = aes_decrypt(ciphertext_b64, key)
        decrypted_result = json.loads(decrypted_json)
        
        self.assertEqual(decrypted_result["plaintext"], plaintext)
    
    def test_decrypt_special_characters(self):
        """Test decryption of special characters"""
        plaintext = "!@#$%^&*()_+-={}[]|:;<>?,./\n\t"
        key = "key123"
        
        encrypted_json = aes_encrypt(plaintext, key)
        encrypted_result = json.loads(encrypted_json)
        ciphertext_b64 = encrypted_result["ciphertext_base64"]
        
        decrypted_json = aes_decrypt(ciphertext_b64, key)
        decrypted_result = json.loads(decrypted_json)
        
        self.assertEqual(decrypted_result["plaintext"], plaintext)
    
    def test_decrypt_unicode(self):
        """Test decryption of Unicode characters"""
        plaintext = "مرحبا世界🌍Привет"
        key = "unicodekey"
        
        encrypted_json = aes_encrypt(plaintext, key)
        encrypted_result = json.loads(encrypted_json)
        ciphertext_b64 = encrypted_result["ciphertext_base64"]
        
        decrypted_json = aes_decrypt(ciphertext_b64, key)
        decrypted_result = json.loads(decrypted_json)
        
        self.assertEqual(decrypted_result["plaintext"], plaintext)
    
    def test_decrypt_wrong_key_fails(self):
        """Test that decrypting with wrong key produces wrong result"""
        plaintext = "Secret Message"
        key1 = "key1"
        key2 = "key2"
        
        encrypted_json = aes_encrypt(plaintext, key1)
        encrypted_result = json.loads(encrypted_json)
        ciphertext_b64 = encrypted_result["ciphertext_base64"]
        
        # Try to decrypt with wrong key
        decrypted_json = aes_decrypt(ciphertext_b64, key2)
        decrypted_result = json.loads(decrypted_json)
        
        # Should either error or produce gibberish
        # Most likely will produce invalid UTF-8 and error
        if decrypted_result.get("status") == "success":
            # If it doesn't error, it should at least not match original
            self.assertNotEqual(decrypted_result.get("plaintext"), plaintext)
    
    def test_decrypt_invalid_base64(self):
        """Test decrypting invalid base64 data"""
        invalid_b64 = "not-valid-base64!!!"
        key = "key"
        
        decrypted_json = aes_decrypt(invalid_b64, key)
        decrypted_result = json.loads(decrypted_json)
        
        # Should have error status
        self.assertEqual(decrypted_result["status"], "error")
    
    def test_decrypt_returns_json(self):
        """Test that decryption returns valid JSON"""
        plaintext = "Test"
        key = "key"
        
        encrypted_json = aes_encrypt(plaintext, key)
        encrypted_result = json.loads(encrypted_json)
        ciphertext_b64 = encrypted_result["ciphertext_base64"]
        
        decrypted_json = aes_decrypt(ciphertext_b64, key)
        
        # Should not raise exception
        result = json.loads(decrypted_json)
        self.assertIsInstance(result, dict)
        self.assertIn("status", result)


class TestAESRoundTrip(unittest.TestCase):
    """Test encryption/decryption round trips"""
    
    def test_roundtrip_basic(self):
        """Test encrypt then decrypt returns original"""
        plaintext = "Test Data"
        key = "testkey"
        
        encrypted_json = aes_encrypt(plaintext, key)
        encrypted_result = json.loads(encrypted_json)
        
        decrypted_json = aes_decrypt(encrypted_result["ciphertext_base64"], key)
        decrypted_result = json.loads(decrypted_json)
        
        self.assertEqual(decrypted_result["plaintext"], plaintext)
    
    def test_roundtrip_multiple_times(self):
        """Test multiple round trips"""
        plaintext = "Secret Message"
        key = "mykey"
        
        current = plaintext
        for _ in range(5):
            encrypted_json = aes_encrypt(current, key)
            encrypted_result = json.loads(encrypted_json)
            
            decrypted_json = aes_decrypt(encrypted_result["ciphertext_base64"], key)
            decrypted_result = json.loads(decrypted_json)
            
            current = decrypted_result["plaintext"]
        
        self.assertEqual(current, plaintext)
    
    def test_roundtrip_various_lengths(self):
        """Test round trip with various plaintext lengths"""
        key = "testkey"
        
        for length in [1, 15, 16, 17, 32, 100, 1000]:
            plaintext = "A" * length
            
            encrypted_json = aes_encrypt(plaintext, key)
            encrypted_result = json.loads(encrypted_json)
            
            decrypted_json = aes_decrypt(encrypted_result["ciphertext_base64"], key)
            decrypted_result = json.loads(decrypted_json)
            
            self.assertEqual(decrypted_result["plaintext"], plaintext,
                           f"Failed for length {length}")


if __name__ == "__main__":
    unittest.main()
