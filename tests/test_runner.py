#!/usr/bin/env python
"""
FEC Test Agent - Test Runner

Comprehensive test runner for all unit tests and integration tests.
Runs all tests and generates a report.
"""

import unittest
import sys
import os
from io import StringIO
import time

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def run_all_tests(verbosity=2):
    """Run all tests and return results"""
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    # Run with detailed output
    runner = unittest.TextTestRunner(verbosity=verbosity, stream=sys.stdout)
    result = runner.run(suite)
    
    return result


def run_specific_test_module(module_name, verbosity=2):
    """Run tests from a specific module"""
    
    try:
        module = __import__(module_name)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        
        return result
    except ImportError as e:
        print(f"Error: Could not import {module_name}: {e}")
        return None


def print_test_summary(result):
    """Print summary of test results"""
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")
    
    print("=" * 70 + "\n")
    
    return result.wasSuccessful()


def main():
    """Main entry point"""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description="FEC Test Agent - Test Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py              # Run all tests
  python test_runner.py --module test_aes_encryption  # Run specific module
  python test_runner.py --quiet      # Run tests with minimal output
  python test_runner.py --verbose    # Run tests with maximum output
        """
    )
    
    parser.add_argument(
        '--module', '-m',
        help='Run tests from specific module (e.g., test_aes_encryption)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Maximum output'
    )
    
    args = parser.parse_args()
    
    # Determine verbosity
    verbosity = 2  # Default
    if args.quiet:
        verbosity = 0
    elif args.verbose:
        verbosity = 2
    
    print("\n" + "=" * 70)
    print("🔐 FEC TEST AGENT - UNIT TEST RUNNER")
    print("=" * 70 + "\n")
    
    start_time = time.time()
    
    # Run tests
    if args.module:
        print(f"Running tests from module: {args.module}\n")
        result = run_specific_test_module(args.module, verbosity=verbosity)
    else:
        print("Running all tests...\n")
        result = run_all_tests(verbosity=verbosity)
    
    elapsed = time.time() - start_time
    
    if result:
        # Print summary
        success = print_test_summary(result)
        print(f"Elapsed time: {elapsed:.2f}s\n")
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
    else:
        print("Failed to run tests\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
