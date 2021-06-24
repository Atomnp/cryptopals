from Crypto.Cipher import AES
from base64 import b64decode
""" in this file we implement algorithm for cbc encryption and decryption """


def xor_bytes(a, b):
    assert len(a) == len(b), "xor_byte's arguments must have equal lengths"
    return bytes([x ^ y for x, y in zip(a, b)])


def pad(message_bytes, block_size=16):
    padding = len(message_bytes) % block_size
    return message_bytes+bytes([padding]*padding)


def getblocks(message_bytes, block_size):
    return [message_bytes[i:i+block_size]
            for i in range(0, len(message_bytes), block_size)]


def encrypt_block_aes(input_bytes, key):
    assert len(input_bytes) == len(
        key), "length of input bytes must equal lenght of key in block aes encryption"
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(input_bytes)


def decrypt_block_aes(block, key):
    assert len(block) == len(
        key), "length of input bytes must equal lenght of key in block aes encryption"
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(block)


def cbc_encrypt(message, key, iv):
    """ message may not be properly padded to the required length that is m """
    # padded_byte = bytes(message, "utf-8")
    padded_bytes = pad(message, block_size=16)
    blocks = getblocks(padded_bytes, 16)
    ciphertext = b""
    for block in blocks:
        """ encrypt the block using simple block encryption technique like AES
            and use encrypted thing as a iv for encryption of next block
         """

        encrypted_byte = encrypt_block_aes(
            xor_bytes(block, iv), key)

        iv = encrypted_byte
        ciphertext += encrypted_byte
    return ciphertext


def cbc_decrypt(message, key, iv):
    blocks = getblocks(message, 16)
    message_text = b""

    for block in blocks:
        decrypted = decrypt_block_aes(block, key)
        message_text += xor_bytes(decrypted, iv)
        iv = block
    return message_text


if __name__ == "__main__":
    key = b"YELLOW SUBMARINE"

    with open("ch2.txt") as f:
        ciphertext = b64decode(
            ''.join([line.strip() for line in f.readlines()]))

    iv = bytes([0x00] * 16)
    decrypted = cbc_decrypt(ciphertext, key, iv)

    print(decrypted.decode('ascii'))
    print(type(decrypted))

    assert(ciphertext == cbc_encrypt(decrypted, key, iv))
