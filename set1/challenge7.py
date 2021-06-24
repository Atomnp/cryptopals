import base64
from Crypto.Cipher import AES

with open("ch7.txt") as file:
    encrypted_text = base64.b64decode(file.read())
key = b'YELLOW SUBMARINE'
cipher = AES.new(key, AES.MODE_ECB)
ans = cipher.decrypt(encrypted_text)
print(ans)
# print(encrypted_text)
