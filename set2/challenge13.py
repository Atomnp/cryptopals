from challenge10 import ecb_encrypt, ecb_decrypt
import os
key = os.urandom(16)


def sanitize(text=""):
    return text.replace('&', '').replace('&', '')


def profile_for(email):
    profile = [('email', email), ('uid', '10'), ('role', 'user')]
    encoded = [k + '=' + sanitize(v) for k, v in profile]
    return '&'.join(encoded)


def parse_profile(encoded):
    fields = encoded.split('&')
    items = [tuple(field.split('=')) for field in fields]
    profile = {key: value for key, value in items}
    return profile


def oracle(email):
    return ecb_encrypt(profile_for(email).encode('ascii'), key)


def isAdmin(token):
    decrypted = ecb_decrypt(token, key).decode("ascii")
    return parse_profile(decrypted)["role"] == "admin"


if __name__ == "__main__":
    """ first craft a technique so that one block should contain admin and some padding characters
        in our examle we will put that admin block in second block of encrypted ecb cipher
        so next we copy that entire admin block and add to other cipher to become admin
    """
    admin_encrypted = oracle('aaaaaaaaaaadmin' + '\x0b' * 11)
    """ email=aaaaaaaaaa
        adminxxxxxxxxxxx  =>assume \x0b to be x for visual purpose
        &uid=10&role=use
        rPPPPPPPPPPPPPPP
        """
    assert(len(admin_encrypted) == 4 * 16)
    admin_block = admin_encrypted[16:32]

    normal_blocks = oracle('aaaaaaaaaaaaa')
    """ email=aaaaaaaaaa
        aaa&uid=10&role=
        userPPPPPPPPPPP   =>this block will be replaced by 'adminXXXXXXXXXXX'
        """
    assert(len(normal_blocks) == 3 * 16)
    """ paste admin block from above as 3rd block  """
    crafted = normal_blocks[:32] + admin_block

    check_admin = isAdmin(crafted)
    print("Logged: %s" % str(check_admin))
