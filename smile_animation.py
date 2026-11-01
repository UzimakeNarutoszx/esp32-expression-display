import time

from smile_geometry import draw_face


def run(display):
    draw_face(display, True)
    print("smile drawn")
    while True:
        time.sleep_ms(2250)
        draw_face(display, False)
        print("blink")
        time.sleep_ms(150)
        draw_face(display, True)
        print("blink")
