from challenge3 import decode_single_xor

# read file line by line
fd = open("ch4.txt", "r")
lines = fd.readlines()
for item in lines:
    print(item)
    final_result = []
    res = decode_single_xor(item[:-1])
print(final_result[:10])
# print(string[300])
