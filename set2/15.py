def unpad(input_bytes, block_size=16):
    last_item = input_bytes[-1]
    if last_item > block_size:
        raise "Bad Padding"
    padding = input_bytes[-last_item:]
    if padding != bytes([last_item]*last_item):
        raise "Bad Padding"
    if last_item <= block_size:
        return input_bytes[:-1*last_item]
    else:
        return input_bytes


if __name__ == "__main__":
    padded = "ICE ICE BABY\x04\x04\x04\x04".encode('ascii')
    unpadded = "ICE ICE BABY".encode('ascii')
    assert(unpadded == unpad(padded))
