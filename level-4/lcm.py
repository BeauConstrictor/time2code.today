def add_multiple(number: float, i: int, multiples):
    multiple = number * i
    if multiples.get(multiple):
        multiples[multiple].add(number)
    else:
        multiples[multiple] = {number}

def lcm(*numbers: float) -> float:
    multiples = {}

    i = 1
    while True:
        for n in numbers:
            add_multiple(n, i, multiples)
            i += 1

            for k, v in multiples.items():
                if len(v) == len(numbers): return k

print(lcm(5, 10))
