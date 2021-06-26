from challenge10 import cbc_decrypt, cbc_encrypt
import os

KEY = os.urandom(16)
IV = os.urandom(16)


def escape(s):
    return s.replace("%", "%37").replace("=", "%61").replace(";", "%59")


def unescape(s):
    return s.replace("%59", ";").replace("%61", "=").replace("%37", "%")


def get_token(userdata):
    prefix = b"comment1=cooking%20MCs;userdata="
    suffix = b";comment2=%20like%20a%20pound%20of%20bacon"
    cookie = prefix + bytes(escape(userdata), "latin-1") + suffix
    return cbc_encrypt(cookie, KEY, IV)


def is_admin(token):
    cookie = cbc_decrypt(token, KEY, IV).decode("latin-1")

    fields = cookie.split(';')
    items = [(key, unescape(value)) for key, value in
             (field.split('=', maxsplit=1) for field in fields
              if "=" in field)]
    return any([item == ('admin', 'true') for item in items])


"""
';'  after last bit flip becomes ':'
'='  after last bit flip becomes '<'  

in cbc mode if we changed any bit in some block of the encrypted cipher text
then while decrypting that cipher text the block where we changed single bit will be
completely scrambled but the blocks after that block will be changed only by fliping
the same bit position which be fliped in the previous block

so in this case since while encrypting ';' and '=' are encode but ':' and '<' are not encoded
so previously while encrypting we give ':' and '<' as as user input but later we will change required bit 
from the cipher text itself to change : to ; and < to =

for that to work we need to scramle one complete block( by fliping required bits) so we add 16 byte block 
just to get desired next block by completely scrambling it

"""
if __name__ == "__main__":
    token = get_token("XXXXXXXXXXXXXXXX:admin<true:XXXX" * 16)
    token = bytearray(token)
    token[32] ^= 0x1
    token[38] ^= 0x1
    token[43] ^= 0x1
    assert(is_admin(bytes(token)))
    print("admin gained sucessfully sucessfulll")
