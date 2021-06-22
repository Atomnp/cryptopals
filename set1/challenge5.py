
def xor_text_with_key(text, key):
    # createing key of length equal  to the length of the text
    complete_key = key*int(len(text)/len(key))
    if len(complete_key) != len(text):
        complete_key += key[:(len(text) % len(key))]
    test = text.encode()
    final = ""
    for x, y in zip(text, complete_key):
        a = hex(ord(x) ^ ord(y))[2:]
        if len(a) == 1:
            a = '0'+a
        final += a
    return final


if __name__ == "__main__":
    text = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""
    key = "ICE"
    ans = xor_text_with_key(text, key)
    print(ans)
