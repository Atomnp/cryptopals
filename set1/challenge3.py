"""

in this problem we are given a hex string, this is a string which obtained
by xoring our message text with single character, we need to brute force xor
with every possible characater and we can find a key and required message

"""
import binascii
from typing import SupportsComplex


def get_score_of_text(text):
    # data that represents frequency of english letters in the plaint text
    english_freq = [
        0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
        0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
        0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
        0.00978, 0.02360, 0.00150, 0.01974, 0.00074
    ]
    letter_counts = {}
    others_count = 0
    for character in text:
        # if current character is english alphaber
        if(character >= ord('a') and character <= ord("z") or character >= ord("A") and character <= ord("Z")):
            if(character >= ord('a')):
                character -= 32
            if character not in letter_counts:
                letter_counts[character] = 0
            else:
                letter_counts[character] += 1
        elif (character >= 32 and character <= 126):
            others_count += int(1)
        elif (character == 9 or character == 10 or character == 13):
            others_count += 1
        else:
            return -1  # impossible that given text is a plain english string
    measure = 0
    alphabet_length = len(text)-others_count
    for key in letter_counts:
        observed_count = letter_counts[key]
        expected_count = alphabet_length * english_freq[key-ord('A')]
        difference = observed_count - expected_count
        measure += difference*difference / expected_count

    return measure*others_count*others_count*others_count*others_count


def xor_hex_strings(str1, str2):
    assert len(str1) == len(
        str2), "Hex string to perform xor should have equal length"
    res = ""
    return "".join([hex((int(x, 16) ^ int(y, 16)))[2:] for (x, y) in zip(str1, str2)])


def decode_single_xor(xs):
    result = []
    for i in range(255):
        a = bytes([i]*int(len(xs)//2))
        res = xor_hex_strings(a.hex(), xs)
        # get_score_of_text(res)
        # print(i)
        # print((bytes.fromhex(res)))
        score = get_score_of_text(bytes.fromhex(res))
        if score != -1:
            result.append((res, score))
    result.sort(key=lambda x: x[1])
    for item in result:
        print(f'{bytes.fromhex(item[0])}: {item[1]}')

    # print(f' key={i} and {bytes.fromhex(res)}')


if __name__ == "__main__":
    b = "0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032"
    decode_single_xor(b)
