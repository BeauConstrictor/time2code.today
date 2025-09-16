from math import factorial
from typing import Iterator, Any
from decimal import getcontext, Decimal
import sys

decimal = getcontext()

def leibniz(digits: int) -> Iterator[Decimal]:
    decimal.prec = digits + 100

    is_add = True
    running_value = Decimal(0)
    iteration = Decimal(1)
    
    while True:
        denominator = iteration * Decimal(2) - Decimal(1)
        term = Decimal(4) / denominator
        
        if not is_add: term *= Decimal(-1)
        running_value += term
        is_add = not is_add
        
        yield running_value
        iteration += Decimal(1)
        
def chudnovsky(digits: int) -> Iterator[Decimal]:
    decimal.prec = digits + 100
    C = 426880 * Decimal(10005).sqrt()

    k = 0
    total = Decimal(0)
    while True:
        numerator = Decimal(factorial(6*k)) * (545140134*k + 13591409)
        denominator = Decimal(factorial(3*k)) * (Decimal(factorial(k))**3) * (640320**(3*k))
        term = numerator / denominator
        if k % 2:
            term = -term
        total += term
        pi_approx = C / total
        yield pi_approx
        k += 1

algorithms = {
    "leibniz": leibniz,
    "chudnovsky": chudnovsky,
}

gui_batch_sizes = {
    "leibniz": 2000,
    "chudnovsky": 1,
}
