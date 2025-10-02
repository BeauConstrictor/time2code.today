from typing import Self
import random
import turtle
import math
import time

SIM_SPEED = 0.0001
SIM_SIZE = 200
COLLISION_TOLERANCE = 1
DRAG = 0.9995

class PhysicsObject:
    def __init__(self, colliders: list[Self]):
        self.x = 0
        self.y = 0
        
        self.vx = 0
        self.vy = 0
        
        self.bounciness = 0.5
        self.drag = DRAG
        
        self.mass = 10
        
        self.colliders = colliders
        
    def step(self, dt):
        self.vy -= self.mass
        
        bound = SIM_SIZE - self.mass / 2
        
        if self.x >= bound or self.x <= -bound:
            self.vx *= -self.bounciness
        if self.y >= bound or self.y <= -bound:
            self.vy *= -self.bounciness
            
        self.vx *= self.drag
        self.vy *= self.drag
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        self.x = sorted([-bound, self.x, bound])[1]
        self.y = sorted([-bound, self.y, bound])[1]
        
class Ball(PhysicsObject):
    def __init__(self, colliders: list[PhysicsObject]):
        super().__init__(colliders)
        
        self.vx = random.randint(-10000, 10000)
        self.vy = random.randint(-10000, 10000)
        
        self.x = random.randint(-100, 100)
        self.y = random.randint(-100, 100)
        
        self.mass = random.randint(10, 50)
        
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.shapesize(self.mass / 20)
        self.turtle.penup()
        
        self.turtle.color(*[random.randint(0, 200) for i in range(3)])
        
    def draw(self):
        self.turtle.goto(self.x, self.y)
        
def main() -> None:
    turtle.tracer(0)
    turtle.colormode(255)
    turtle.bgcolor("black")
    
    bg = turtle.Turtle()
    bg.shape("square")
    bg.shapesize(SIM_SIZE / 20 * 2)
    bg.color("white")
    bg.stamp()
    bg.hideturtle()
    
    balls = []
    
    for i in range(100):
        balls.append(Ball(balls))
        
    previous_time = time.perf_counter()
        
    while True:
        current_time = time.perf_counter()
        elapsed = current_time - previous_time
        
        dt = elapsed * SIM_SPEED
                
        for b in balls:
            b.step(dt)
            b.draw()
            
        turtle.update()
        
if __name__ == "__main__":
    main()