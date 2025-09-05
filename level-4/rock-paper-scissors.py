import random
from time import sleep

BEATS = {
    "r": "s",
    "p": "r",
    "s": "p",
}

LONG = {
    "r": "rock",
    "p": "paper",
    "s": "scissors"
}

ALLOWED = list("rps")

def get_choice(prompt) -> str:
    while True:
        choice = input(prompt)
        normalised = choice.strip()[0]
        if normalised in ALLOWED: return normalised
        print("enter a valid play!")

def main():
    while True:
        computer = random.choice(ALLOWED)
        player = get_choice("Enter your play: ")
        print("wait for it...")
        sleep(1)
        print("...")
        sleep(1)
        print("...")
        sleep(1)
        print(f"The computer chose {LONG[computer]}!")
        sleep(1)

        outcome = "beats" if BEATS[player] == computer else "loses to"
        print(f"{LONG[player]} {outcome} {LONG[computer]},")
        if BEATS[player] == computer:
            print("you win!")
        else:
            print("you lose!")

if __name__ == "__main__":
    main()
