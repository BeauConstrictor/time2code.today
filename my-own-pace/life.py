import os
from time import sleep

class Life:
    def __init__(self, board_file: str) -> None:
        self.load_board(board_file)
        
    def load_board(self, board_file: str) -> None:
        with open(board_file, "r") as f:
            lines = [line.rstrip("\n") for line in f if line.strip()]
        
        row_lengths = {len(line) for line in lines}
        if len(row_lengths) != 1:
            raise ValueError(f"Inconsistent row lengths in {board_file}: {row_lengths}")

        valid_chars = {"#", ".", " "}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c not in valid_chars:
                    raise ValueError(f"Invalid character '{c}' at ({x}, {y}) in {board_file}")

        self.board = [[c == "#" for c in line] for line in lines]

    @staticmethod
    def keep_alive(cell: bool, neighbours: int) -> bool:
        if neighbours < 2:
            return False
        elif neighbours == 2:
            return cell
        elif neighbours == 3:
            return True
        elif neighbours > 3:
            return False
            
    @staticmethod
    def count_neighbours(x: int, y: int, board: list[list[bool]], allow_wrapping: bool = False) -> int:
        height = len(board)
        width = len(board[0])
        living_neighbours = 0

        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue  # skip the cell itself

                nx = x + dx
                ny = y + dy

                if allow_wrapping:
                    nx %= width
                    ny %= height
                else:
                    if nx < 0 or ny < 0 or nx >= width or ny >= height:
                        continue  # skip out-of-bounds

                if board[ny][nx]:
                    living_neighbours += 1

        return living_neighbours
        
    def step(self, allow_wrapping: bool) -> None:
        new_frame = [
            [self.keep_alive(cell, self.count_neighbours(x, y, self.board))
            for x, cell in enumerate(row)]
            for y, row in enumerate(self.board)
        ]
        
        for y, row in enumerate(self.board):
            for x, is_alive in enumerate(row):
                neighbours = self.count_neighbours(x, y, self.board, allow_wrapping)
                new_frame[y][x] = self.keep_alive(is_alive, neighbours)
            
        self.board = new_frame
        
    def draw(self, with_ascii: bool=False) -> None:
        output = "\033[2J\033[H"
        output += "Conway's Game of Life\n\n"
        
        horizontal_border = "--" * len(self.board[0]) if with_ascii else "──" * len(self.board[0])
        output += f"+-{horizontal_border}-+\n" if with_ascii else f"┌─{horizontal_border}─┐\n"
        
        vertical_border = "|" if with_ascii else "│"
            
        for row in self.board:
            output += f"{vertical_border} "
            for is_alive in row:
                if with_ascii:
                    output += "##" if is_alive else "  "
                else:
                    output += "██" if is_alive else "  "
            output += f" {vertical_border}\n"
        
        output += f"+-{horizontal_border}-+" if with_ascii else f"└─{horizontal_border}─┘"
        print(output)
        
def get_yn(prompt: str) -> bool:
    response = (input(prompt + "[y/N] ( )\b\b").strip().lower() + " ")[0]
    return response == "y"
        
if __name__ == "__main__":
    board_path = os.path.join(".life", input("Board name: ").strip() + ".board")
    ascii_only = get_yn("Use ASCII only mode? ")
    wrapping = get_yn("do you want wrapping? ")
    slow_mode = get_yn("do you want slow mode? ")
    
    game = Life(board_path)
    while True:
        try:
            game.draw(ascii_only)
            game.step(wrapping)
            
            if slow_mode:
                input()
            else:
                sleep(0.025)
        except KeyboardInterrupt:
            break