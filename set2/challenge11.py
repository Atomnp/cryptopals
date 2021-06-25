import os
import random
from challenge2 import cbc_encrypt, ecb_encrypt, getblocks


def random_mode_encryptor(message_bytes):
    """ 
    generate random key and ramdom vector insert some random bytes to the front and back of the input
    randomly select mode of encryption to encrypt the message and encrypt with that mode and return
    encrypted text along with mode of encryption to check later if our guess about mode of encryption was right

    """
    key = os.urandom(16)
    iv = os.urandom(16)

    prefix = os.urandom(random.randint(5, 10))
    suffix = os.urandom(random.randint(5, 10))

    message_bytes = prefix+message_bytes+suffix

    mode = random.choice(["ECB", "CBC"])
    encrypted = (ecb_encrypt(message_bytes, key)
                 if mode == "ECB" else cbc_encrypt(message_bytes, key, iv))
    return encrypted, mode


if __name__ == "__main__":
    """ 
    generate random bytes for the message encrypt it using random encryptor
    predict the mode of encryption and check if prediction is right 
    """
    message_bytes = bytes([0x55]*40)
    ciphertext, mode_of_encryption = random_mode_encryptor(message_bytes)
    blocks = getblocks(ciphertext, block_size=16)
    predicion = ""
    if len(set(blocks)) < len(blocks):
        print("Prediction :ECB")
        predicion = "ECB"
    else:
        print("Prediciton CBC")
        predicion = "CBC"
    if(predicion == mode_of_encryption):
        print("And you are right")
    else:
        print("And you are wrong")
