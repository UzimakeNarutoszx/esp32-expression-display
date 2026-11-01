from micropython import const

WIDTH = const(240)
HEIGHT = const(280)
Y_OFFSET = const(20)

BG = 0x1082
YELLOW = 0xFFE0
DARK = 0x0000


def _rgb565_bytes(color):
    return bytes((color >> 8, color & 0xFF))


def _isqrt(value):
    if value <= 1:
        return value
    guess = value
    next_guess = (guess + 1) // 2
    while next_guess < guess:
        guess = next_guess
        next_guess = (guess + value // guess) // 2
    return guess


def _window(display, x, y, width, height):
    display.set_window(x, y + Y_OFFSET, width, height)


def fill(display, color):
    display.fill(color)


def rect(display, x, y, width, height, color):
    if width <= 0 or height <= 0:
        return
    _window(display, x, y, width, height)
    row = _rgb565_bytes(color) * width
    display.write_pixels(row * height)


def circle(display, cx, cy, radius, color):
    radius_sq = radius * radius
    for y in range(cy - radius, cy + radius + 1):
        dy = y - cy
        span = _isqrt(radius_sq - dy * dy)
        rect(display, cx - span, y, span * 2 + 1, 1, color)


def draw_face(display, eyes_open=True):
    fill(display, BG)
    circle(display, WIDTH // 2, HEIGHT // 2, 92, YELLOW)

    if eyes_open:
        rect(display, 72, 105, 20, 30, DARK)
        rect(display, 148, 105, 20, 30, DARK)
    else:
        rect(display, 68, 119, 28, 6, DARK)
        rect(display, 144, 119, 28, 6, DARK)

    # Upward-curved smile, built from short horizontal strokes.
    rect(display, 86, 188, 68, 8, DARK)
    rect(display, 78, 181, 10, 15, DARK)
    rect(display, 154, 181, 10, 15, DARK)
    rect(display, 88, 196, 64, 8, DARK)


def draw_red_test(display):
    fill(display, 0xF800)
