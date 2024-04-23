# import required libraries
import math
import sys
from collections import Counter


# define functions
def load_text_file(path):
    with open(path, 'r', encoding='utf-8') as archive:
        return archive.read()


def calculate_entropy_from_text(text):
    frequencies = Counter(text)
    total_characters = sum(frequencies.values())

    return -sum((freq / total_characters) * math.log2(freq / total_characters) for char, freq in frequencies.items())


def count_unique_characters_from_text(text):
    unique_characters = set(text)
    return len(unique_characters)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_entropy.py <path_to_file>")
        sys.exit(1)

    path = sys.argv[1]
    text = load_text_file(path)

    number = count_unique_characters_from_text(text)
    print("Unique characters of text file:", number)

    entropy = calculate_entropy_from_text(text)
    print("Entropy of text file:", entropy)
