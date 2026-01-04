"""
Quick Start Guide - Running Tests

This file provides quick commands for running the FEC Test Agent unit tests.
"""

# ============================================================================
# QUICK START - RUNNING TESTS
# ============================================================================

# Navigate to the tests directory
# cd tests

# ============================================================================
# RUN ALL TESTS
# ============================================================================

# Using test_runner.py (recommended)
python test_runner.py

# Using unittest discovery
python -m unittest discover

# ============================================================================
# RUN SPECIFIC TEST MODULE
# ============================================================================

# AES Encryption Tests
python test_runner.py --module test_aes_encryption
python -m unittest test_aes_encryption

# Reed-Solomon Tests
python test_runner.py --module test_reed_solomon
python -m unittest test_reed_solomon

# Convolution Encoding Tests
python test_runner.py --module test_convolution
python -m unittest test_convolution

# CCSDS FEC Tests
python test_runner.py --module test_ccsds_fec
python -m unittest test_ccsds_fec

# Integration Tests
python test_runner.py --module test_integration
python -m unittest test_integration

# ============================================================================
# RUN SPECIFIC TEST CLASS
# ============================================================================

# AES Encryption class
python -m unittest test_aes_encryption.TestAESEncryption
python -m unittest test_aes_encryption.TestAESDecryption
python -m unittest test_aes_encryption.TestAESRoundTrip

# Reed-Solomon classes
python -m unittest test_reed_solomon.TestReedSolomonEncoding
python -m unittest test_reed_solomon.TestReedSolomonDecoding
python -m unittest test_reed_solomon.TestReedSolomonRoundTrip

# CCSDS Convolutional
python -m unittest test_ccsds_fec.TestCCSDSConvolutionalCode

# CCSDS Reed-Solomon
python -m unittest test_ccsds_fec.TestCCSDSReedSolomon

# Integration tests
python -m unittest test_integration.TestToolJSONResponses
python -m unittest test_integration.TestSuccessStatuses
python -m unittest test_integration.TestErrorHandling

# ============================================================================
# RUN SPECIFIC TEST METHOD
# ============================================================================

# AES encryption basic test
python -m unittest test_aes_encryption.TestAESEncryption.test_encrypt_basic

# Reed-Solomon roundtrip test
python -m unittest test_reed_solomon.TestReedSolomonRoundTrip.test_roundtrip_basic

# Convolution encoding test
python -m unittest test_convolution.TestConvolutionEncoding.test_encode_rate_1_2

# CCSDS RS test
python -m unittest test_ccsds_fec.TestCCSDSReedSolomon.test_ccsds_rs255_223_encode

# ============================================================================
# VERBOSITY OPTIONS
# ============================================================================

# Quiet mode (minimal output)
python test_runner.py --quiet
python -m unittest discover -q

# Verbose mode (detailed output)
python test_runner.py --verbose
python -m unittest discover -v

# ============================================================================
# INDIVIDUAL TEST FILE EXECUTION
# ============================================================================

# Run test file directly
python test_aes_encryption.py
python test_reed_solomon.py
python test_convolution.py
python test_ccsds_fec.py
python test_integration.py

# ============================================================================
# TEST FILTERING
# ============================================================================

# Run tests matching pattern
python -m unittest discover -k "test_encrypt"
python -m unittest discover -k "test_roundtrip"

# ============================================================================
# OUTPUT WITH TIMING
# ============================================================================

# Run with timing (using test_runner.py)
python test_runner.py

# This shows:
# - Total tests run
# - Number of successes, failures, errors
# - Elapsed time

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

# If tests fail:
# 1. Check that you're in the tests/ directory
# 2. Verify parent directory is in Python path
# 3. Check dependencies are installed: pip install -r ../requirements.txt
# 4. Run verbose mode to see details: python test_runner.py --verbose

# If import errors occur:
# 1. Ensure __init__.py exists in tests/
# 2. Check tools/ directory exists in parent directory
# 3. Verify Python version >= 3.8

# ============================================================================
# COMMON COMMANDS SUMMARY
# ============================================================================

"""
SUMMARY OF COMMON COMMANDS:

Run all tests:
    python test_runner.py

Run specific module:
    python test_runner.py --module test_aes_encryption

Run specific class:
    python -m unittest test_aes_encryption.TestAESEncryption

Run specific test:
    python -m unittest test_aes_encryption.TestAESEncryption.test_encrypt_basic

Quiet output:
    python test_runner.py --quiet

Verbose output:
    python test_runner.py --verbose

Run tests with unittest:
    python -m unittest discover
    python -m unittest discover -v

For more help:
    python test_runner.py --help
    python -m unittest --help
"""
