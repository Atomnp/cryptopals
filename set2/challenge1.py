def pkcs_padding(input_bytes, required_length):
    n = required_length-len(input_bytes)
    input_bytes += bytes([n])*n
    return input_bytes


if __name__ == "__main__":
    key = b"YELLOW SUBMARINE"
    out = pkcs_padding(key, 20)
    print(out)
