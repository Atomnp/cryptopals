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
