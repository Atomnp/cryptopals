from set1.challenge3 import decode_single_xor
# read file line by line
fd = open("ch4.txt", "r")
lines = fd.readlines()
final_result = []
for item in lines:
    print(item)
    result = decode_single_xor(item[:-1])
    final_result += result
for item in final_result:
    print(f'{bytes.fromhex(item[0])}: {item[1]}')
