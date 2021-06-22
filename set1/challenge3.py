"""

in this problem we are given a hex string, this is a string which obtained
by xoring our message text with single character, we need to brute force xor
with every possible characater and we can find a key and required message

"""
import binascii
from typing import SupportsComplex


def get_english_score(input_bytes):
    """Compares each input byte to a character frequency
    chart and returns the score of a message based on the
    relative frequency the characters occur in the English
    language.
    """

    # From https://en.wikipedia.org/wiki/Letter_frequency
    # with the exception of ' ', which I estimated.
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    return sum([character_frequencies.get(chr(byte), 0) for byte in input_bytes.lower()])


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


def xor_hex_strings(input_bytes, char_value):
    output_bytes = b''
    for byte in input_bytes:
        output_bytes += bytes([byte ^ char_value])
    return output_bytes


def decode_single_xor(xs):
    potential_messages = []
    for key_value in range(256):
        message = xor_hex_strings(xs, key_value)
        score = get_english_score(message)
        data = {
            'message': message,
            'score': score,
            'key': key_value
        }
        potential_messages.append(data)
    score_sorted_list = sorted(
        potential_messages, key=lambda x: x['score'], reverse=True)
    return score_sorted_list[0]


if __name__ == "__main__":
    # b = "1fee0a3945563d2b5703701817584b5f5b54702522f5031b561929ea2d1e"
    text = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    res = decode_single_xor(bytes.fromhex(text))
    print(res["message"])
