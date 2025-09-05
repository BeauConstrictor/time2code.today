charmap = list("0123456789ABCDEF")

def getnum(prompt: str) -> int:
    while True:
        num = input(prompt).strip()
        try:
            return int(num)
        except ValueError:
            print("enter a valid number!")


def to_base(decimal: int, base: int) -> str:
    binary = ""
    while decimal > 0:
        remainder = decimal % base
        binary = charmap[remainder] + binary
        decimal = decimal // base
    return binary

def main():
    base = getnum("enter an output base: ")
    num = getnum("DECIMAL = ")
    print(f"-> BASE {base} = {to_base(num, base)}")

if __name__ == "__main__":
    main()
