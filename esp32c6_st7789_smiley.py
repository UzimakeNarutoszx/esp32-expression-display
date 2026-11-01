from machine import Pin, SoftSPI
import time

WIDTH = 172
HEIGHT = 320
OFFSET_X = 0
CS = Pin(14, Pin.OUT, value=1)
DC = Pin(15, Pin.OUT, value=0)
RST = Pin(21, Pin.OUT, value=1)
BL = Pin(22, Pin.OUT, value=1)
SPI_BUS = SoftSPI(baudrate=2_000_000, polarity=0, phase=0, sck=Pin(7), mosi=Pin(6), miso=Pin(5))


def command(value, data=b""):
    CS.value(0)
    DC.value(0)
    SPI_BUS.write(bytes((value,)))
    if data:
        DC.value(1)
        SPI_BUS.write(data)
    CS.value(1)


def reset_display():
    CS.value(0)
    time.sleep_ms(50)
    RST.value(0)
    time.sleep_ms(10)
    RST.value(1)
    time.sleep_ms(10)
    command(0x11)
    time.sleep_ms(100)
    command(0x36, b"\x00")
    command(0x3A, b"\x55")
    command(0xB0, b"\x00\xE8")
    command(0xB2, b"\x0C\x0C\x00\x33\x33")
    command(0xB7, b"\x75")
    command(0xBB, b"\x1A")
    command(0xC0, b"\x80")
    command(0xC2, b"\x01\xFF")
    command(0xC3, b"\x13")
    command(0xC4, b"\x20")
    command(0xC6, b"\x0F")
    command(0xD0, b"\xA4\xA1")
    command(0xE0, b"\xD0\x0D\x14\x0D\x0D\x09\x38\x44\x4E\x3A\x17\x18\x2F\x30")
    command(0xE1, b"\xD0\x09\x0F\x08\x07\x14\x37\x44\x4D\x38\x15\x16\x2C\x2E")
    command(0x21)
    command(0x29)
    command(0x2C)
    command(0x36, b"\x48")


def window(x, y, width, height):
    x += OFFSET_X
    command(0x2A, bytes((x >> 8, x & 255, (x + width - 1) >> 8, (x + width - 1) & 255)))
    command(0x2B, bytes((y >> 8, y & 255, (y + height - 1) >> 8, (y + height - 1) & 255)))
    command(0x2C)


def fill_rect(x, y, width, height, color):
    if width <= 0 or height <= 0:
        return
    window(x, y, width, height)
    row = color.to_bytes(2, "big") * width
    CS.value(0)
    DC.value(1)
    for _ in range(height):
        SPI_BUS.write(row)
    CS.value(1)


def fill(color):
    for y in range(0, HEIGHT, 8):
        fill_rect(0, y, WIDTH, min(8, HEIGHT - y), color)


def circle(cx, cy, radius, color):
    radius_sq = radius * radius
    for y in range(cy - radius, cy + radius + 1):
        dy = y - cy
        span = int((radius_sq - dy * dy) ** 0.5)
        fill_rect(cx - span, y, span * 2 + 1, 1, color)


reset_display()
fill(0xFFE0)
circle(86, 160, 64, 0xFFE0)
fill_rect(62, 135, 14, 22, 0x0000)
fill_rect(96, 135, 14, 22, 0x0000)
fill_rect(62, 195, 48, 8, 0x0000)
fill_rect(56, 188, 8, 16, 0x0000)
fill_rect(108, 188, 8, 16, 0x0000)
print("ST7789 SMILEY DRAWN")
