"""
Convolution Encoding Example

Demonstrates basic convolutional code with rate 1/2.
"""


def convolution_encode_example():
    """Example: Encode data with Convolution code"""
    input_bits = [1, 0, 1, 1, 0, 1, 0, 0]
    generator_polynomial = [0o7, 0o5]  # (7,5) octal - rate 1/2
    
    # Simple convolution encoding
    encoded = []
    state = 0
    constraint_length = 3
    
    for bit in input_bits:
        state = ((state << 1) | bit) & ((1 << constraint_length) - 1)
        
        # Calculate output bits
        for gen in generator_polynomial:
            parity = 0
            temp_state = state
            for i in range(constraint_length):
                if (gen >> i) & 1:
                    parity ^= (temp_state >> i) & 1
            encoded.append(parity)
    
    # Add tail bits
    for _ in range(constraint_length - 1):
        state = (state << 1) & ((1 << (constraint_length - 1)) - 1)
        for gen in generator_polynomial:
            parity = 0
            temp_state = state
            for i in range(constraint_length):
                if (gen >> i) & 1:
                    parity ^= (temp_state >> i) & 1
            encoded.append(parity)
    
    # Convert to string
    input_str = ''.join(str(b) for b in input_bits)
    encoded_str = ''.join(str(b) for b in encoded)
    
    print("=" * 60)
    print("🔀 Convolution Encoding Example (Rate 1/2)")
    print("=" * 60)
    print(f"Input Bits: {input_str}")
    print(f"Input Length: {len(input_bits)} bits")
    print(f"Generator Polynomial: (7,5) octal")
    print(f"Constraint Length: {constraint_length}")
    print(f"Code Rate: 1/2")
    print(f"Encoded Bits: {encoded_str}")
    print(f"Encoded Length: {len(encoded)} bits")
    print(f"Expansion Ratio: {len(encoded) / len(input_bits):.1f}x")
    print()
    
    return encoded_str, input_str


def convolution_rate_13_example():
    """Example: Rate 1/3 convolutional code (higher protection)"""
    input_bits = [1, 0, 1, 1, 0, 1]
    generator_polynomial = [0o7, 0o5, 0o3]  # Rate 1/3
    
    # Simple convolution encoding
    encoded = []
    state = 0
    constraint_length = 3
    
    for bit in input_bits:
        state = ((state << 1) | bit) & ((1 << constraint_length) - 1)
        
        for gen in generator_polynomial:
            parity = 0
            temp_state = state
            for i in range(constraint_length):
                if (gen >> i) & 1:
                    parity ^= (temp_state >> i) & 1
            encoded.append(parity)
    
    # Add tail bits
    for _ in range(constraint_length - 1):
        state = (state << 1) & ((1 << (constraint_length - 1)) - 1)
        for gen in generator_polynomial:
            parity = 0
            temp_state = state
            for i in range(constraint_length):
                if (gen >> i) & 1:
                    parity ^= (temp_state >> i) & 1
            encoded.append(parity)
    
    input_str = ''.join(str(b) for b in input_bits)
    encoded_str = ''.join(str(b) for b in encoded)
    
    print("=" * 60)
    print("🔀 Convolution Encoding Example (Rate 1/3)")
    print("=" * 60)
    print(f"Input Bits: {input_str}")
    print(f"Input Length: {len(input_bits)} bits")
    print(f"Generator Polynomial: (7,5,3) octal")
    print(f"Constraint Length: {constraint_length}")
    print(f"Code Rate: 1/3 (Higher Error Protection)")
    print(f"Encoded Bits: {encoded_str}")
    print(f"Encoded Length: {len(encoded)} bits")
    print(f"Expansion Ratio: {len(encoded) / len(input_bits):.1f}x")
    print()


def convolution_comparison():
    """Example: Compare different code rates"""
    input_bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]
    constraint_length = 3
    
    print("=" * 60)
    print("📊 Convolution Code Rate Comparison")
    print("=" * 60)
    print(f"Input: {len(input_bits)} bits")
    print()
    
    # Rate 1/2
    rate_12_output = len(input_bits) * 2 + (constraint_length - 1) * 2
    print(f"Rate 1/2: {rate_12_output} bits output (100% overhead)")
    
    # Rate 1/3
    rate_13_output = len(input_bits) * 3 + (constraint_length - 1) * 3
    print(f"Rate 1/3: {rate_13_output} bits output (200% overhead)")
    
    # Rate 1/4
    rate_14_output = len(input_bits) * 4 + (constraint_length - 1) * 4
    print(f"Rate 1/4: {rate_14_output} bits output (300% overhead)")
    
    print()
    print("Higher rate (1/2) = Less overhead, Less error protection")
    print("Lower rate (1/3) = More overhead, Better error protection")
    print()


if __name__ == "__main__":
    # Rate 1/2
    encoded_12, input_str = convolution_encode_example()
    
    # Rate 1/3
    convolution_rate_13_example()
    
    # Comparison
    convolution_comparison()
