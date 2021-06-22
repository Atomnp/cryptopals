import base64

""" 
to convert any data into base64 we must understand few things, base64 is mostly

Base64 encoding schemes are commonly used when there is a need to encode binary data that needs be 
stored and transferred over media that are designed to deal with textual data. This is to ensure that 
the data remains  intact without modification during transport.

Ascii base64 and hex all are ways to represetent binary data as text
In ascii one character can represent 1 byte
in hex 2 character are required to represent 1 byte
by using clever technique base64 require 4 character to represent 3 byte so it is for efficient than hex

If there is hex string given, we must first know its binary representation and then use that binary
and encode it in base64 

"""

hexstr = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
# encoded = base64.encode(bytes.fromhex(hexstr))
encoded = base64.b64encode(bytes.fromhex(hexstr))


def good():
    return "good"


print(encoded.decode())
