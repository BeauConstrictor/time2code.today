from math import pi, factorial, sqrt
from typing import Iterator, Any
from decimal import getcontext, Decimal
import time

DIGITS = 77_994

decimal = getcontext()
decimal.prec = DIGITS

C = 426880 * Decimal(10005).sqrt()

def leibniz() -> Iterator[Decimal]:
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
        
def chudnovsky() -> Iterator[Decimal]:
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
        
def ansii_verify_approx(approx_pi: str, pi: str, incorrect_digits: int) -> tuple[str, int]:
    output = "\033[1;32m"
    correct_characters = 0
    
    for i, c in enumerate(approx_pi):
        if i >= len(pi):
            output += "\033[0m"
            output += approx_pi[correct_characters:]
            break
        reference_c = pi[i]
        if c == reference_c:
            output += reference_c
            correct_characters += 1
        else:
            output += f"\033[0m\033[0;31m"
            output += approx_pi[correct_characters:]
            output += "\033[0m"
            break

    return output, correct_characters
        
def every_nth(generator: Iterator[Any], n: int) -> Iterator[Any]:
    for i, val in enumerate(generator, 1):
        if i % n == 0:
            yield val
      
def main() -> None: 
    with open(".reference-pi.txt", "r") as f:
        pi_str = f.read()

    for approx_pi in every_nth(chudnovsky(), 10):
        output, correct_digits = ansii_verify_approx(str(approx_pi), pi_str, 10)
        
        print("\033[2J")
        print(f"Correct Digits: {correct_digits}")
        print(output)
    
def watch_convergence() -> None:
    digit_idx = 2003
    
    with open(".reference-pi.txt", "r") as f:
        pi_str = f.read()
        
    for approx_pi in chudnovsky():
        digits = str(approx_pi)
        _, correct_digits = ansii_verify_approx(digits, pi_str, 10)
        
        if correct_digits > digit_idx + 100: break
        
        digit = digits[digit_idx]
        print(digit)
    
if __name__ == "__main__":
    main()