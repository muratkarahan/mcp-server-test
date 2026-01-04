#!/usr/bin/env python3
"""
Script to create a binary file test.bin in the same directory and write four hex bytes: 0x1A, 0xCF, 0xFC, 0x1D.
"""

import pathlib

def main():
    workspace = pathlib.Path(__file__).parent
    target = workspace / "test.bin"
    target.write_bytes(bytes([0x1A, 0xCF, 0xFC, 0x1D]))
    print(f"{target} created with content: 1A CF FC 1D.")

if __name__ == "__main__":
    main()
