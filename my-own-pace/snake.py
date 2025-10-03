import turtle
import random
from enum import Enum

SIZE = 20
FRAMERATE = 10

interval = 1000 // FRAMERATE

class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

def lerp_color(c1: tuple[float, float, float], c2: tuple[float, float, float], t: float)-> tuple[float, float, float]:
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))

class Snake:
    def __init__(self) -> None:
        self.positions = [(i, 0) for i in range(5)]
        self.direction = Direction.RIGHT
        self.eaten_apple = False
        
        self.game_over = False
        self.score = 0
        
        self.apples = []
        self.add_apple()
        
        self.turtle = turtle.Turtle()
        self.turtle.shape("square")
        self.turtle.hideturtle()
        self.turtle.penup()
        
        self.score_counter = turtle.Turtle()
        self.score_counter.color("white")
        self.score_counter.hideturtle()
        self.score_counter.penup()
        self.score_counter.goto(0, -SIZE*10 - 80)
        
    def add_apple(self) -> None:
        while True:
            pos = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
            if pos not in self.positions: break
        self.apples = [pos]
        
    def draw_score(self) -> None:
        self.score_counter.clear()
        self.score_counter.write(str(self.score),
                                 align="center",
                                 font=("Arial", 32, "bold"))
                                 
    def trigger_game_over(self) -> None:
        self.score_counter.clear()
        self.score_counter.color("red")
        self.score_counter.write(str(self.score),
                                 align="center",
                                 font=("Arial", 32, "bold"))
        self.game_over = True
        
    def move(self) -> None:
        old_pos = self.positions[-1]
        offset = self.direction.value
        new_pos = (old_pos[0] + offset[0], old_pos[1] + offset[1])
        
        if new_pos in self.positions:
            self.trigger_game_over()
        if min(new_pos) < 0 or max(new_pos) > SIZE-1:
            self.trigger_game_over()
        
        if new_pos in self.apples:
            self.apples.remove(new_pos)
            self.add_apple()
            self.eaten_apple = True
            self.score += 1
        
        self.positions.append(new_pos)
        if not self.eaten_apple: self.positions.pop(0)
        self.eaten_apple = False
        
    def draw(self) -> None:
        self.turtle.clear()
        
        offset = SIZE * 10
        
        for row in range(SIZE):
            for col in range(SIZE):
                if (col, row) in self.apples:
                    self.turtle.color("red")
                    self.turtle.goto(col * 20 - offset, row * 20 - offset)
                    self.turtle.stamp()
                if (col, row) in self.positions:
                    t = self.positions.index((col, row)) / len(self.positions)
                    a = (0, 1, 0)
                    b = (0, 0.5, 0)
                    self.turtle.color(lerp_color(a, b, t))
                    self.turtle.goto(col * 20 - offset, row * 20 - offset)
                    self.turtle.stamp()
                    
        self.draw_score()

def init_turtle() -> None:
    turtle.bgcolor("black")
    turtle.tracer(0)
    turtle.update()
    
    bg = turtle.Turtle()
    bg.shapesize(SIZE)
    bg.shape("square")
    bg.goto(-10, -10)
    bg.color("white")
    bg.hideturtle()
    bg.stamp()

def go_up(snake: Snake) -> None:
    if snake.direction != Direction.DOWN:
        snake.direction = Direction.UP

def go_down(snake: Snake) -> None:
    if snake.direction != Direction.UP:
        snake.direction = Direction.DOWN

def go_left(snake: Snake) -> None:
    if snake.direction != Direction.RIGHT:
        snake.direction = Direction.LEFT

def go_right(snake: Snake) -> None:
    if snake.direction != Direction.LEFT:
        snake.direction = Direction.RIGHT

def update(snake: Snake) -> None:
        snake.move()
        if snake.game_over:
            turtle.done()
        snake.draw()
        turtle.update()
        
        turtle.ontimer(lambda: update(snake), interval)

def main() -> None:
    init_turtle()
    snake = Snake()
    
    turtle.onkey(lambda: go_up(snake), "Up")
    turtle.onkey(lambda: go_down(snake), "Down")
    turtle.onkey(lambda: go_left(snake), "Left")
    turtle.onkey(lambda: go_right(snake), "Right")
    turtle.listen()

    update(snake)
    turtle.done()

if __name__ == "__main__":
    main()
