import os
import sys

BOARD_WIDTH = 20
BOARD_HEIGHT = 20

def draw_board(board, cursor):
    os.system("cls" if os.name == "nt" else "clear")
    cx, cy = cursor
    for y, row in enumerate(board):
        line = ""
        for x, cell in enumerate(row):
            if (x, y) == (cx, cy):
                line += "[" + ("#" if cell else ".") + "]"
            else:
                line += " " + ("#" if cell else ".") + " "
        print(line)
    print("\nUse WASD to move, SPACE to toggle, Q to quit and save.")

if os.name == "nt":
    import msvcrt
    def getch():
        return msvcrt.getch().decode("utf-8").lower()
else:
    import tty
    import termios
    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

def save_board(board, filename):
    with open(filename, "w") as f:
        for row in board:
            f.write("".join("#" if cell else "." for cell in row) + "\n")
    print(f"Board saved to {filename}!")

def main():
    board = [[False for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    cursor = (0, 0)

    while True:
        draw_board(board, cursor)
        key = getch()

        x, y = cursor
        if key == "w" and y > 0:
            cursor = (x, y - 1)
        elif key == "s" and y < BOARD_HEIGHT - 1:
            cursor = (x, y + 1)
        elif key == "a" and x > 0:
            cursor = (x - 1, y)
        elif key == "d" and x < BOARD_WIDTH - 1:
            cursor = (x + 1, y)
        elif key == " ":
            board[y][x] = not board[y][x]
        elif key == "q":
            filename = input("Enter filename to save: ").strip()
            save_board(board, os.path.join(".life", filename + ".board"))
            break

if __name__ == "__main__":
    main()
