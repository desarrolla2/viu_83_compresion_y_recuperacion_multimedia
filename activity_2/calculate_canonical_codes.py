# import required libraries
import sys
import heapq
from collections import Counter
from tabulate import tabulate


# define functions
def load_text_file(path):
    with open(path, 'r', encoding='utf-8') as archive:
        return archive.read()


def calculate_frequencies_and_probabilities_from_text(text):
    frequencies = Counter(text)
    total_characters = sum(frequencies.values())
    probabilities = {char: freq / total_characters for char, freq in frequencies.items()}
    return frequencies, probabilities


def build_huffman_tree(frequencies):
    heap = [[weight, [symbol, ""]] for symbol, weight in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def generate_canonical_codes(symbols):
    symbols.sort(key=lambda x: (len(x[1]), x[0]))
    canonical_codes = {}
    code = 0
    length = len(symbols[0][1])

    for sym in symbols:
        current_length = len(sym[1])
        if current_length > length:
            code <<= (current_length - length)
            length = current_length
        canonical_codes[sym[0]] = {'code': bin(code)[2:].zfill(length), 'probability': probabilities[sym[0]]}
        code += 1

    return canonical_codes


def escape_special_characters(char):
    if char == '\n':
        return '\\n'  # Newline
    elif char == '\t':
        return '\\t'  # Tab
    elif char == '\r':
        return '\\r'  # Carriage return
    elif char == '\0':
        return '\\0'  # Null character
    elif ord(char) < 32 or ord(char) == 127:  # Other non-printable characters
        return f'\\x{ord(char):02x}'  # Hex code
    return char


def print_canonical_codes(canonical_codes):
    table = []
    total_expected_length = 0

    for char, info in canonical_codes.items():
        char_escaped = escape_special_characters(char)
        char_code_length = len(info['code'])
        char_weighted_length = char_code_length * info['probability']

        total_expected_length += char_weighted_length

        table.append(
            [char_escaped, info['code'], f"{info['probability']:.4f}", char_code_length, f"{char_weighted_length:.4f}"]
        )

    print(tabulate(table, headers=['Character', 'Code', 'Probability', 'Length', 'P * L'], tablefmt='grid'))

    print("The average length of each character in bits of text file:", f"{total_expected_length:.4f}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_canonical_codes.py <path_to_file>")
        sys.exit(1)

    path = sys.argv[1]
    text = load_text_file(path)
    frequencies, probabilities = calculate_frequencies_and_probabilities_from_text(text)
    huffman_tree = build_huffman_tree(frequencies)
    canonical_codes = generate_canonical_codes(huffman_tree)
    print_canonical_codes(canonical_codes)
