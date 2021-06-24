def repetition_count(text, block_size):
    blocks = [text[i:i+block_size] for i in range(0, len(text), block_size)]
    return len(blocks)-len(set(blocks))


if __name__ == "__main__":
    prev_max_count = 0
    ecb_encrypted = ""

    with open("ch8.txt") as file:
        lines = file.read().splitlines()

    for ciphertext in lines:
        count = repetition_count(ciphertext, block_size=16)
        if count > prev_max_count:
            ecb_encrypted = ciphertext
            prev_max_count = count
    print(count)
