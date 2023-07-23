# A simple application to find collisions in the last x bytes of the output of a PRG.
# 
# Usage: python FindMagicNumbers.py <file_name> <number_of_bytes>
# Author: sreejith.naarakathil@gmail.com

import sys
import re

def read_file(file_name):
    with open(file_name, 'r') as file:
        data = file.readlines()
    return data

def extract_numbers(data):
    random_numbers = []
    for line in data:
        if line.strip():
            out2 = line.split()[2].strip()
            random_numbers.append(out2)
    return random_numbers

def check_repeating(numbers, num_bytes):
    repeating_numbers = {}
    for idx, num in enumerate(numbers):
        last_bytes = num[-2*num_bytes:]  # Since each byte is represented by 2 hexadecimal characters
        if last_bytes in repeating_numbers:
            repeating_numbers[last_bytes].append(idx)
        else:
            repeating_numbers[last_bytes] = [idx]
    return repeating_numbers

def find_repeating_numbers_pair(repeating_numbers):
    count = 0
    index_pairs = []
    for key in repeating_numbers:
        if len(repeating_numbers[key]) > 1:
            count += 1
            index_pairs.extend([(repeating_numbers[key][i] + 1, repeating_numbers[key][i + 1] + 1) for i in range(len(repeating_numbers[key]) - 1)])
    return count, index_pairs

def main():
    if len(sys.argv) != 3:
        print("Usage: python FindMagicNumbers.py <file_name> <number_of_bytes>")
        return

    file_name = sys.argv[1]
    num_bytes = int(sys.argv[2])

    data = read_file(file_name)
    random_numbers = extract_numbers(data)
    repeating_numbers = check_repeating(random_numbers, num_bytes)
    count, index_pairs = find_repeating_numbers_pair(repeating_numbers)

    print(f'Total number of collision of the last {num_bytes} bytes: {count}')
    print(f'Pairs of indices where collision occurs: {index_pairs}')

if __name__ == '__main__':
    main()
