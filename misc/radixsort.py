
def sort(l: list[int]) -> list[int]:
    max_bit_width = max([n.bit_length() for n in l]) + 1

    for i in range(max_bit_width):
        all_1s = []
        all_0s = []

        for n in l:
            bit = n & (1 << i)

            if bit == 0: all_0s.append(n)
            else:        all_1s.append(n)

        l = all_0s + all_1s

    return l

if __name__ == "__main__":
    print(sort([2, 5, 1, 32, 7, 4, 1, 7, 2, 213, 5, 45]))
