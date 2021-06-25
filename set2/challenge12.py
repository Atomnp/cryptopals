from base64 import b64decode
from os import urandom
from challenge10 import ecb_encrypt, getblocks

secret = b64decode(
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
    "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
    "YnkK")
# secret = b"my"
key = urandom(16)


def oracle(input):
    return ecb_encrypt(input+secret, key=key)


def determine_block_size(oracle):
    """ to determine the block size we continuously call oracle function
    with different lentth argument, when the size of the output cipher text
    changes that means one new block is added to the cipher text
    now if we subtract this new leght with newly added block with previous lenght
    of cipher text we can get teh size block size of the cipher text
     """
    size = len(oracle(bytes()))
    i = 1
    while size == len(oracle(bytes([0x42]*i))):
        i += 1
    size_with_one_extra_block = len(oracle(bytes([0x42]*i)))
    return size_with_one_extra_block-size


def get_last_known_block(plaintext, block_size):
    """ return last block-size'd  characters from the secret that we have decrypted
    which is present in the plaintext 

    when running for the first time it returns only padding 16 characters long
    'BBBBBBBBBBBBBBBB' ==>len =16

    if our plain text is  'mynameisaayushneupane'
    it returns : 'eisaayushneupane'

    if plain text is    'myname'
    it returns 'BBBBBBBBBmyname'



    """
    PADDING_CHAR = 0x42
    ans = plain_text[-1*block_size:]
    front_padding = block_size-len(ans)
    return bytes([PADDING_CHAR]*front_padding)+ans


def get_target_block(plaintext, block_size):
    """
        when we continue decrypting message mynameisaayushneupane and lets say block size is 4
        then at any point we may be decrypting any one block of 'myna meis aayu shne upan e'
        this function returns currenctly active block that means tyo vanda agadi ko block
        haru decrypt gari sakim. and suitable padding requred to obtain next character pani
        return garxa forexampe hami 3rd block ko 'aa' samma chai decrypt garim re aba 'u' decrypt 
        garnu xa vane it returns 2 for the block index and 'B' as padding. 

        4th  block ko all 4 characters decrypt garna 
        3 BBB ==> (blocksize-1) 'B' to decrypt first character of block  
        3 BB  ==>  (blocksize-2) 'B' to decrypt first character of block  
        ...
        ...

        return garxa.


    """
    PADDING_BYTE = 0x42
    current_index = len(plain_text)
    block_index = current_index // block_size

    offset_inside_block = current_index % block_size
    padding = block_size-1-offset_inside_block

    pad = bytes([PADDING_BYTE]*padding)
    return block_index, pad


if __name__ == "__main__":
    """ 
    #create one random key
    #encrypt some message by ecb mode using this key, in this problem messaage is given
    # but it is given in base64 so that hami le suru mai nadekham vanera, now we have to decrypt 
    #this encrypted message

    #for that to work 
    1. determine the size of block from the encrypted message
    2. verify that the mode used is ecb using previous techniques
    3. if we know the block size and we have access to encrypting function of AES mode we can
        perform clever bruteforcing to determine the original message

    # """
    block_size = determine_block_size(oracle)
    plain_text = b""
    for _ in range((len(oracle(bytes())))):
        last_known_block = get_last_known_block(plain_text, block_size)
        target_block_index, pad = get_target_block(
            plain_text, block_size)
        ciphertext = oracle(pad)
        prefix = last_known_block[1:]
        actual_block = getblocks(ciphertext, block_size)[target_block_index]
        for byte in range(256):
            guess = getblocks(oracle(prefix+bytes([byte])), block_size)[0]
            match_found = False

            if guess == actual_block:
                plain_text += bytes([byte])
                match_found = True
                break
        """
            when we continue finding original secret characters one by one and react the last character
            of the secret and then try to find the next character the character will be 0x01 because
            last character find garne bela maa thyakka block size bileko hunxa ani tespaxi euta lai left ko 
            block maa lagepaxi 0x01 ko padding hunxa kinaki single padding character required hunxa

            when we again try yo fetch next character paddin is changed od 0x02 0x02  but agadi ko prefix maa ta
            0x01 gayeko tyo, jun xai padding vayeko le next maa aafai pani change vayera 0x02 vayo so aba 
            target block sanga hamro match hudaina cox
            
            somemessage0x020x02
            somemessage0x01{x in range(256)}

            yo duita compaare garna khojdai hunxum jun maa chai second last byte nai matching xaina so last lai matra
            brute force garera match huna sakdaina, so by this way we determine the end aba last maa euta padding character
            ie 0x01 chai plain text maa aai sakeko le teslai hatayepaxi hami required message recover garna sakxam


        """
        if not match_found:
            assert(plain_text[-1] == 0x01)
            plain_text = plain_text[:-1]
            print(plain_text)
            break
    assert(secret == plain_text)
