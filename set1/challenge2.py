""" Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c
... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965
... should produce:

746865206b696420646f6e277420706c6179 """


def xor_hex_strings(str1, str2):
    assert len(str1) == len(
        str2), "Hex string to perform xor should have equal length"
    res = ""
    return "".join([hex((int(x, 16) ^ int(y, 16)))[2:] for (x, y) in zip(str1, str2)])


# testing
str1 = "1c0111001f010100061a024b53535009181c"
str2 = "686974207468652062756c6c277320657965"

res = xor_hex_strings(str1, str2)
print(res)
