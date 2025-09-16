from typing import Iterator, Any, Callable
from types import ModuleType
from pathlib import Path
import argparse
import sys

import const_pi
import const_e

simple_output = False

modules = {
    "pi": const_pi,
    "e": const_e,
}

def get_reference(constant: str) -> str:
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys._MEIPASS) # type: ignore
    else:
        base_dir = Path(__file__).resolve().parent

    file_path = base_dir / "references" / f"{constant}.txt"

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def ansii_verify_approx(calculation: str, ref: str, incorrect_digits: int) -> tuple[str, int]:
    output = "\033[1;32m"
    correct_characters = 0
    
    for i, c in enumerate(calculation):
        if i >= len(ref):
            output += "\033[0m"
            output += calculation[correct_characters:]
            break
        reference_c = ref[i]
        if c == reference_c:
            output += reference_c
            correct_characters += 1
        else:
            output += f"\033[0m\033[0;31m"
            output += calculation[correct_characters:correct_characters+incorrect_digits]
            output += "\033[0m"
            break

    output += "\033[0m"
    if "." in calculation: correct_characters -= 1
    return output, correct_characters
        
def get_yn(prompt: str) -> bool:
    response = (input(prompt + "[Y/n] ( )\b\b").strip().lower() + " ")[0]
    return response != "n"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="const-crunch", description="Calculate various "
    "mathematial constants to arbitrary precisions.")

    parser.add_argument("constant")
    parser.add_argument("-a", "--algorithm",
                        help="Select an algorithm to compute the constant with")
    parser.add_argument("-f", "--fast", action='store_true',
                        help="Reduce I/O to increase speed")
    parser.add_argument("-l", "--list", action='store_true',
                        help="List supported algorithms for a specific constant")
    parser.add_argument("-d", "--digits", default=100, type=int,
                        help="How many digits to use when during calculation")

    return parser.parse_args()

def verify_args(args: argparse.Namespace) -> bool:
    module = modules.get(args.constant)

    if module is None:
        msg = f"const-crunch: error: unknown constant specified: '{args.constant}'\n\n" \
               "Supported constants:\n\t"
        msg += "\n\t".join(modules.keys())
        print(msg, file=sys.stderr)
        return False

    if args.algorithm is None and not args.list:
        msg = "const-crunch: error: no algorithm supplied\n\nSupported algorithms:\n\t"
        msg += "\n\t".join(module.algorithms)
        print(msg, file=sys.stderr)
        return False

    algo = module.algorithms.get(args.algorithm, None)

    if algo is None and not args.list:
        msg = f"const-crunch: error: unknown algorithm specified: '{args.algorithm}'\n\n" \
               "Supported algorithms:\n\t"
        msg += "\n\t".join(module.algorithms)
        print(msg, file=sys.stderr)
        return False
    
    return True

def calculate(const: str, digits: int, algo: Callable[[int], Iterator[float]]) -> None:
    if not simple_output:
        print("\033[?1049h", sys.stderr)

    last_percentage = 0

    for i in algo(digits):
        string = str(i)[:digits+1]
        if "." not in string: string = string[:digits]
        if string.endswith("."): string = string[:-1]
        ref = get_reference(const)
        output, correct_chars = ansii_verify_approx(string, ref, 200)

        if simple_output:
            percentage = int(correct_chars / digits * 10) * 10
            if percentage != last_percentage:
                last_percentage = percentage
                print(f"{percentage}%", file=sys.stderr)
        else:
            percentage = round(correct_chars / digits * 100, 2)
            print("\033[2J" + f"{output}\n\nCorrect Digits: {correct_chars} / {digits}"
                              f"\nCompletion: {percentage}%", file=sys.stderr)

        if correct_chars == digits:
            if not simple_output:
                print("\033[?1049l", file=sys.stderr)
            print(string)
            break
        

def main() -> None:
    global simple_output

    args = parse_args()
    simple_output = args.fast

    if args.constant == "list":
        print("\n".join(modules.keys()))
        exit(0)

    if args.constant == "gui":
        import gui
        app = gui.App()
        app.mainloop()
        exit(0)

    if not verify_args(args): exit(1)

    module = modules[args.constant]
    algo = module.algorithms.get(args.algorithm, None)

    if args.list:
        print("\n".join(module.algorithms.keys()))
        exit(0)

    if not simple_output:
        if not get_yn(f"const-crunch: calculating {args.digits} digits of "
                      f"{args.constant} using the {args.algorithm} algorithm, "
                      f"correct? "):
            print("aborted.", file=sys.stderr)
            exit(1)

    try:
        calculate(args.constant, args.digits, algo)
    except KeyboardInterrupt:
        if not simple_output:
            print("\033[?1049l", end="", file=sys.stderr)
        print("\n\naborted.", file=sys.stderr)
        exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(file=sys.stderr)
        pass
