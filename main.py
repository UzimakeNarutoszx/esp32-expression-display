import time
from machine import Pin, SPI

from smile_geometry import WIDTH, HEIGHT, Y_OFFSET

CS_PIN = 5
DC_PIN = 3
RST_PIN = 4
SCK_PIN = 1
MOSI_PIN = 2


class ST7789:
    def __init__(self):
        self.cs = Pin(CS_PIN, Pin.OUT, value=1)
        self.dc = Pin(DC_PIN, Pin.OUT, value=0)
        self.rst = Pin(RST_PIN, Pin.OUT, value=1)
        self.spi = SPI(1, baudrate=40_000_000, polarity=0, phase=0,
                       bits=8, firstbit=SPI.MSB,
                       sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=None)
        self.reset()
        self.init_panel()

    def _cmd(self, value, data=b""):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytes((value,)))
        if data:
            self.dc.value(1)
            self.spi.write(data)
        self.cs.value(1)

    def reset(self):
        self.rst.value(1)
        time.sleep_ms(20)
        self.rst.value(0)
        time.sleep_ms(120)
        self.rst.value(1)
        time.sleep_ms(120)

    def init_panel(self):
        self._cmd(0x01)
        time.sleep_ms(150)
        self._cmd(0x11)
        time.sleep_ms(120)
        self._cmd(0x3A, b"\x55")
        self._cmd(0x36, b"\x00")
        self._cmd(0xB0, b"\x00\xF0")
        self._cmd(0xB2, b"\x0C\x0C\x00\x33\x33")
        self._cmd(0xB7, b"\x35")
        self._cmd(0xBB, b"\x19")
        self._cmd(0xC0, b"\x2C")
        self._cmd(0xC2, b"\x01")
        self._cmd(0xC3, b"\x12")
        self._cmd(0xC4, b"\x20")
        self._cmd(0xC6, b"\x0F")
        self._cmd(0xD0, b"\xA4\xA1")
        self._cmd(0xE0, b"\xF0\x09\x13\x12\x12\x2B\x3C\x44\x4B\x1B\x18\x17\x1D\x21")
        self._cmd(0xE1, b"\xF0\x09\x13\x0C\x0D\x27\x3B\x44\x4D\x0B\x17\x17\x1D\x21")
        self._cmd(0x13)
        time.sleep_ms(10)
        self._cmd(0x21)  # display inversion on for IPS glass
        self._cmd(0x29)
        time.sleep_ms(50)

    def set_window(self, x, y, width, height):
        x2 = x + width - 1
        y2 = y + height - 1
        self._cmd(0x2A, bytes((x >> 8, x & 0xFF, x2 >> 8, x2 & 0xFF)))
        self._cmd(0x2B, bytes((y >> 8, y & 0xFF, y2 >> 8, y2 & 0xFF)))
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(b"\x2C")
        self.dc.value(1)

    def write_pixels(self, data):
        self.cs.value(0)
        self.spi.write(data)
        self.cs.value(1)

    def fill(self, color):
        pixel = bytes((color >> 8, color & 0xFF))
        row = pixel * WIDTH
        self.set_window(0, Y_OFFSET, WIDTH, HEIGHT)
        chunk = row * 16
        full_chunks, remainder = divmod(HEIGHT, 16)
        for _ in range(full_chunks):
            self.spi.write(chunk)
        if remainder:
            self.spi.write(row * remainder)
        self.cs.value(1)


# Board power and backlight rails, both active-high on this module.
Pin(15, Pin.OUT, value=1)
Pin(6, Pin.OUT, value=1)

display = ST7789()
print("display ready")
display.fill(0xFFE0)
print("yellow #FFFF00")
while True:
    time.sleep_ms(1000)
