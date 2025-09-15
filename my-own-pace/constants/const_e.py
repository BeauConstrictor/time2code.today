from decimal import Decimal, getcontext
from typing import Iterator
from math import factorial

decimal = getcontext()

def taylor_series(digits: int):
    decimal.prec = 1_000_000
    total = Decimal(0)
    factorial_value = Decimal(1)
    n = 0
    while True:
        if n > 0:
            factorial_value *= Decimal(n)
        total += Decimal(1) / factorial_value
        n += 1
        yield total

def compound_limit(digits: int) -> Iterator[Decimal]:
    decimal.prec = digits + 100
    n = 1
    while True:
        yield (Decimal(1) + Decimal(1)/Decimal(n)) ** Decimal(n)
        n += 1

def continued_fraction(digits: int):
    from decimal import Decimal, getcontext
    decimal.prec = digits + 20

    def a(n):
        if n == 0:
            return 2
        elif n % 3 == 2:
            return 2 * ((n + 1) // 3)
        else:
            return 1

    p0, p1 = 2, 3  # first two numerators
    q0, q1 = 1, 1  # first two denominators
    n = 1

    while True:
        an = a(n)
        p2 = an * p1 + p0
        q2 = an * q1 + q0
        yield Decimal(p2) / Decimal(q2)
        p0, p1 = p1, p2
        q0, q1 = q1, q2
        n += 1

algorithms = {
    "limit": compound_limit,
    "fraction": continued_fraction,
    "taylor": taylor_series,
}