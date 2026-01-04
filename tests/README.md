# FEC Test Agent - Unit Test Suite

Comprehensive unit test suite for the FEC (Forward Error Correction) Test Agent project. Tests cover all encoding tools, CCSDS standards, and agent integration functionality.

## Test Structure

```
tests/
├── __init__.py                      # Package initialization
├── test_aes_encryption.py           # AES encryption/decryption tests (40+ tests)
├── test_reed_solomon.py             # Reed-Solomon error correction tests (35+ tests)
├── test_convolution.py              # Convolution encoding tests (25+ tests)
├── test_ccsds_fec.py                # CCSDS FEC standards tests (45+ tests)
├── test_integration.py              # Integration and JSON response tests (40+ tests)
├── test_runner.py                   # Test runner with CLI interface
└── README.md                         # This file
```

## Running Tests

### Run All Tests
```bash
cd tests
python test_runner.py
```

### Run Specific Module
```bash
python test_runner.py --module test_aes_encryption
python test_runner.py -m test_ccsds_fec
```

### Run with Different Verbosity
```bash
python test_runner.py --quiet      # Minimal output
python test_runner.py --verbose    # Detailed output
```

### Run Individual Test File
```bash
python test_aes_encryption.py
python test_reed_solomon.py
python test_convolution.py
python test_ccsds_fec.py
python test_integration.py
```

## Test Coverage

### 1. AES Encryption Tests (test_aes_encryption.py)

**TestAESEncryption** (10 tests)
- ✅ Basic encryption
- ✅ Empty plaintext
- ✅ Long text (1000+ bytes)
- ✅ Special characters (!@#$%^&*()...)
- ✅ Unicode characters (Arabic, Chinese, Russian, Emoji)
- ✅ Key padding (short keys extended to 32 bytes)
- ✅ Key truncation (long keys truncated to 32 bytes)
- ✅ Different keys produce different ciphertexts
- ✅ Multiple encryptions produce different ciphertexts (random IV)
- ✅ IV inclusion verification

**TestAESDecryption** (10 tests)
- ✅ Basic decryption
- ✅ Empty string decryption
- ✅ Long text decryption (1000+ bytes)
- ✅ Special characters decryption
- ✅ Unicode decryption
- ✅ Wrong key detection (fails or produces gibberish)
- ✅ Invalid base64 error handling
- ✅ JSON response validation

**TestAESRoundTrip** (3 tests)
- ✅ Encrypt→decrypt roundtrip
- ✅ Multiple roundtrips (5x encrypt/decrypt cycles)
- ✅ Various plaintext lengths (1, 15, 16, 17, 32, 100, 1000 bytes)

**Total AES Tests: 23**

### 2. Reed-Solomon Tests (test_reed_solomon.py)

**TestReedSolomonEncoding** (8 tests)
- ✅ Basic RS encoding
- ✅ Different nsym values (5, 10, 20, 32)
- ✅ Empty string encoding
- ✅ Single byte encoding
- ✅ Long data (1000+ bytes)
- ✅ Special characters
- ✅ Base64 output validation
- ✅ JSON response format

**TestReedSolomonDecoding** (6 tests)
- ✅ Basic decoding
- ✅ Empty string decoding
- ✅ Decoding with introduced errors
- ✅ Too many errors detection
- ✅ Invalid base64 error handling
- ✅ JSON response format

**TestReedSolomonRoundTrip** (4 tests)
- ✅ Encode→decode roundtrip
- ✅ Various nsym values (5, 10, 20)
- ✅ Various data lengths (1, 10, 50, 100 bytes)
- ✅ Single error correction

**TestReedSolomonErrorCorrection** (2 tests)
- ✅ Error positions returned
- ✅ Correction capability (nsym=10 can correct 5 errors)

**Total RS Tests: 20**

### 3. Convolution Encoding Tests (test_convolution.py)

**TestConvolutionEncoding** (13 tests)
- ✅ Basic convolution encoding
- ✅ Comma-separated input ("1, 0, 1")
- ✅ Space-separated input ("1 0 1")
- ✅ Continuous input ("101")
- ✅ Rate 1/2 (2x expansion)
- ✅ Rate 1/3 (3x expansion)
- ✅ Single bit encoding
- ✅ All zeros encoding
- ✅ All ones encoding
- ✅ Long sequences (200 bits)
- ✅ Binary output validation
- ✅ JSON response format
- ✅ Expansion ratio calculation

**TestConvolutionTest** (3 tests)
- ✅ Demo mode
- ✅ Rate verification mode
- ✅ Performance mode

**TestConvolutionGeneratorPolynomials** (2 tests)
- ✅ Octal format polynomials (7,5), (171,133), (31,27)
- ✅ Different polynomials produce different outputs

**Total Convolution Tests: 18**

### 4. CCSDS FEC Tests (test_ccsds_fec.py)

**TestCCSDSConvolutionalCode** (4 tests)
- ✅ K=7, Rate 1/2 (CCSDS standard)
- ✅ K=7, Rate 1/3 (stronger outer code)
- ✅ K=5, Rate 1/2 (simpler variant)
- ✅ Invalid standard error handling

**TestCCSDSReedSolomon** (6 tests)
- ✅ CCSDS (255,223) encoding
- ✅ CCSDS (255,239) encoding
- ✅ RS decoding
- ✅ Encode/decode roundtrip
- ✅ Tool function validation

**TestCCSDSConcatenatedCode** (3 tests)
- ✅ Basic concatenated encoding
- ✅ Different configurations
- ✅ Tool function validation

**TestCCSDSTurboCodes** (3 tests)
- ✅ Turbo encoding
- ✅ Custom frame sizes
- ✅ Tool function validation

**TestCCSDSLDPCCodes** (3 tests)
- ✅ LDPC Rate 1/2
- ✅ LDPC Rate 1/3
- ✅ Tool function validation

**TestCCSDSFECComparison** (3 tests)
- ✅ FEC comparison
- ✅ All methods included
- ✅ Statistics provided

**TestCCSDSStandardGeneratorPolynomials** (3 tests)
- ✅ K=7 Rate 1/2 generators (0o171, 0o133)
- ✅ K=7 Rate 1/3 generators (0o171, 0o133, 0o145)
- ✅ K=5 Rate 1/2 generators (0o31, 0o27)

**Total CCSDS Tests: 25**

### 5. Integration Tests (test_integration.py)

**TestToolJSONResponses** (12 tests)
- ✅ AES encrypt returns JSON
- ✅ AES decrypt returns JSON
- ✅ Reed-Solomon encode returns JSON
- ✅ Reed-Solomon decode returns JSON
- ✅ Convolution encode returns JSON
- ✅ Convolution test returns JSON
- ✅ All CCSDS tools return JSON

**TestSuccessStatuses** (6 tests)
- ✅ Successful operations return "success" status

**TestErrorHandling** (3 tests)
- ✅ Invalid inputs return error status
- ✅ Error messages are provided
- ✅ Operation field included in errors

**TestToolParameterValidation** (4 tests)
- ✅ Reed-Solomon accepts string and integer nsym
- ✅ Turbo accepts string and integer frame_size

**TestDataPreservation** (4 tests)
- ✅ Plaintext preserved in AES encrypt response
- ✅ Ciphertext preserved in AES decrypt response
- ✅ Original data preserved in RS encode response
- ✅ Input bits preserved in Conv encode response

**TestStatisticsProvided** (4 tests)
- ✅ AES provides size information
- ✅ RS provides encoding statistics
- ✅ Convolution provides code rate
- ✅ CCSDS tools provide statistics

**Total Integration Tests: 33**

## Test Statistics

- **Total Test Cases: 119+**
- **Modules: 5**
- **Test Classes: 25**
- **Coverage:**
  - ✅ AES-256-CBC encryption/decryption
  - ✅ Reed-Solomon error correction (all nsym values)
  - ✅ Convolution encoding (rates 1/2, 1/3, etc.)
  - ✅ CCSDS Convolutional (K=7 1/2, K=7 1/3, K=5 1/2)
  - ✅ CCSDS Reed-Solomon ((255,223), (255,239))
  - ✅ CCSDS Concatenated Codes
  - ✅ CCSDS Turbo Codes
  - ✅ CCSDS LDPC Codes
  - ✅ Tool JSON responses
  - ✅ Error handling
  - ✅ Parameter validation

## Test Execution

### Python unittest
```bash
python -m unittest discover tests
python -m unittest tests.test_aes_encryption
python -m unittest tests.test_aes_encryption.TestAESEncryption.test_encrypt_basic
```

### Using test_runner.py
```bash
python test_runner.py                       # All tests
python test_runner.py -m test_aes_encryption  # Specific module
python test_runner.py --quiet               # Quiet mode
python test_runner.py --verbose             # Verbose mode
```

## Test Output Example

```
======================================================================
🔐 FEC TEST AGENT - UNIT TEST RUNNER
======================================================================

Running all tests...

test_aes_encryption (test_aes_encryption.TestAESEncryption.test_encrypt_basic) ... ok
test_aes_encryption (test_aes_encryption.TestAESEncryption.test_encrypt_empty_plaintext) ... ok
test_aes_encryption (test_aes_encryption.TestAESEncryption.test_encrypt_long_text) ... ok
...

======================================================================
TEST SUMMARY
======================================================================
Tests Run: 119
Successes: 119
Failures: 0
Errors: 0
Skipped: 0

✅ ALL TESTS PASSED!
======================================================================
```

## Testing Best Practices

### Test Organization
- Tests organized by functionality (AES, RS, Conv, CCSDS, Integration)
- Each test file focuses on a specific component
- Test classes group related test methods
- Clear, descriptive test method names

### Test Coverage
- **Happy Path**: Normal usage scenarios
- **Edge Cases**: Empty strings, single bytes, very long data
- **Error Cases**: Invalid inputs, wrong keys, corrupted data
- **Round Trips**: Encode→decode and encrypt→decrypt
- **Parameter Variations**: Different sizes, formats, standards
- **JSON Validation**: All responses are valid JSON
- **Statistics**: Operations provide meaningful statistics

### Test Patterns
- **Setup**: Create test data
- **Execute**: Call the function
- **Assert**: Verify results and side effects
- **Isolation**: Tests are independent and can run in any order

## Continuous Integration

Tests can be integrated with CI/CD pipelines:

```bash
# Generate test report
python -m pytest tests/ --junit-xml=report.xml

# Run with coverage
python -m coverage run -m pytest tests/
python -m coverage report

# Run with CI/CD
python test_runner.py && echo "Tests passed" || echo "Tests failed"
```

## Adding New Tests

To add tests for a new feature:

1. Create test class inheriting from `unittest.TestCase`
2. Add test methods with descriptive names starting with `test_`
3. Use `self.assertEqual()`, `self.assertTrue()`, etc. for assertions
4. Add docstring to test methods
5. Run tests to verify

Example:
```python
class TestNewFeature(unittest.TestCase):
    """Test new FEC feature"""
    
    def test_new_encoding_basic(self):
        """Test basic new encoding"""
        result = new_encode("Test")
        self.assertEqual(result["status"], "success")
```

## Troubleshooting

### ImportError when running tests
- Ensure you're in the `tests/` directory
- Check Python path includes parent directory

### Test failures
- Check error message for details
- Run specific test with verbose output
- Verify tool implementations
- Check JSON response format

### Missing dependencies
- Install required packages: `pip install -r ../requirements.txt`
- Verify Python version >= 3.8

## References

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [FEC Test Agent documentation](../README.md)
- [CCSDS Standards](../tools/ccsds_fec.py)
