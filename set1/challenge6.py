from typing import final
from set1.challenge3 import decode_single_xor
import base64


def distance(s1, s2):
    """ returns the hamming distance between two strings in their binary representatin """
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    diff = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            # xor gives 1 when two bits are different so we are counting numbers of ones
            # to count number of bits that are different in bytes
            diff += bin(s1[i] ^ s2[i]).count("1")
    return diff


def predict_key_size(ciphertext):
    """ 
        to predict the key size used to generate the cipher text we perform bruteforce from key of size 2
        then we calculate the hamming distance between two consecutive key-size'd byte from the cipher text
        to get accurate result we calculate the hamming distance of each two consecutive byte without repeating
        ie 1st and second byte , 3rd and 4th byte we then average the hamming distance of each consecutive byte
        then we perform normalization by dividin by key size
        the key-size which produce least normalized hamming distance is the best guess for the size of key
    """

    key_data = []

    for key_size in range(2, 41):
        res = [ciphertext[i:i+key_size]
               for i in range(0, len(ciphertext), key_size)]
        count = 0
        total_distance = 0
        for i in range(0, len(res), 2):
            if (i+1) < len(res) and len(res[i]) == len(res[i+1]):
                total_distance += distance(res[i], res[i+1])
                count += 1
        average_distance = total_distance/count
        normalized = average_distance/key_size
        key_data.append({"key_size": key_size, "score": normalized})
    key_data_sorted = sorted(key_data, key=lambda x: x["score"])
    return key_data_sorted[0]["key_size"]


def repeating_xor_bytes_with_key(input_bytes, key_bytes):
    """ input_bytes: plain text in bytes form
        key_bytes: key to xor with in bytes form

        returns: bytes that is the result of repeating xor of input bytes with
        given key
    """

    output_bytes = b""
    complete_key = key_bytes*int(len(input_bytes)/len(key_bytes))
    complete_key += key[:len(input_bytes) % len(key_bytes)]

    for i in range(len(input_bytes)):
        output_bytes += bytes([input_bytes[i] ^ complete_key[i]])
    return output_bytes


def get_chunks(ciphertext, key_size):
    """ 
    this function given the cipher text and key size returns the chunks
    chunks here refers to for example of string of first byte of each key-size'd byte
    of the cypher text

    example :
    ciphertext=abcdefghi
    keysize=3

    first separate the cipher into group of 3
    abc def ghi

    then one chunk is first byte of all group ie adg second chunk is second byte of all group
    ie beh an so on

     """

    res = [ciphertext[i:i+key_size]
           for i in range(0, len(ciphertext), key_size)]
    result = []
    for i in range(key_size):
        mystr = b""
        for item in res:
            if i < len(item):
                mystr += bytes([item[i]])
        result.append(mystr)
    return result


if __name__ == "__main__":
    file = open("ch6.txt", "r")
    # data = file.read()
    ciphertext = base64.b64decode(file.read())

    # splits string by number of characters
    key_size = predict_key_size(ciphertext)

    ans = get_chunks(ciphertext, key_size)
    """ 
    after getting the chunks we try to determine most probable key for
    each chunks and combinint most probable key for each chunk gives us the complete
    key
     """
    key = b""
    for item in ans:
        key += bytes([decode_single_xor(item)["key"]])
    """ after gettting the key we xor it with cipher text to get original message """
    out = repeating_xor_bytes_with_key(ciphertext, key)

    print("end")
