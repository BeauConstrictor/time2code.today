from tkinter import Canvas
import turtle

def int_to_col(n: int) -> str:
    if n == -1:
        return "#000000"
    c = int(n * 255 / 100)
    return f"#{c:02x}{c:02x}{c:02x}"

def scale(value, pixel_max, target_min, target_max):
    return target_min + (value / pixel_max) * (target_max - target_min)

def mandelbrot_colour(x: float, y: float) -> int:
    zx = 0
    zy = 0

    for i in range(100):
        new_zx = zx**2 - zy**2 + x
        zy = 2 * zx * zy + y
        zx = new_zx

        if zx**2 + zy**2 > 4:
            return i
    
    return -1

def mandelbrot() -> list[list[int]]:
    mandelbrot_set = []

    WIDTH = 1000
    HEIGHT = 1000

    for py in range(HEIGHT):
        row = []
        for px in range(WIDTH):
            x = scale(px, WIDTH, -2.0, 1.0)
            y = scale(py, HEIGHT, -1.5, 1.5)
            row.append(mandelbrot_colour(x, y))
        mandelbrot_set.append(row)


    return mandelbrot_set

def init_turtle() -> Canvas:
    turtle.hideturtle()
    turtle.bgcolor("#020202")
    turtle.penup()
    screen = turtle.Screen()
    screen.tracer(False)
    canvas = screen.getcanvas()
    return canvas

def draw_pixel(canvas, x: int, y: int, color: str) -> None:
    canvas.create_line(x, y, x+1, y, fill=color)

def main() -> None:
    canvas = init_turtle()

    mandelbrot_set = mandelbrot()

    center_offset = len(mandelbrot_set) // 2

    for y, row in enumerate(mandelbrot_set):
        for x, i in enumerate(row):
            draw_pixel(canvas, x-center_offset, y-center_offset, int_to_col(i))

    turtle.done()

if __name__ == "__main__":
    main()