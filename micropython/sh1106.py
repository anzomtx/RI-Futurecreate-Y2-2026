# sh1106.py - Driver for SH1106 OLED display
import framebuf
import time

class SH1106:
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MVLSB)
        self.init_display()

    def init_display(self):
        self.write_cmd(0xAE)  # Display off
        self.write_cmd(0x20, 0x00)  # Set memory addressing mode
        self.write_cmd(0xB0)  # Set page start address
        self.write_cmd(0xC8)  # Set COM output scan direction
        self.write_cmd(0x00, 0x10)  # Set column address range
        self.write_cmd(0x40)  # Set display start line
        self.write_cmd(0x81, 0xCF)  # Set contrast control
        self.write_cmd(0xA1)  # Set segment re-map
        self.write_cmd(0xA6)  # Display normal (not inverted)
        self.write_cmd(0xA8, 0x3F)  # Set multiplex ratio
        self.write_cmd(0xD3, 0x00)  # Set display offset
        self.write_cmd(0xD5, 0x80)  # Set display clock divide ratio/oscillator frequency
        self.write_cmd(0xD9, 0xF1)  # Set pre-charge period
        self.write_cmd(0xDA, 0x12)  # Set COM pins hardware configuration
        self.write_cmd(0xDB, 0x40)  # Set VCOMH deselect level
        self.write_cmd(0x8D, 0x14)  # Enable charge pump
        self.write_cmd(0xAF)  # Display on
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(0xAE)

    def poweron(self):
        self.write_cmd(0xAF)

    def contrast(self, contrast):
        self.write_cmd(0x81, contrast)

    def invert(self, invert):
        self.write_cmd(0xA7 if invert else 0xA6)

    def write_cmd(self, *args):
        self.i2c.writeto_mem(self.addr, 0x00, bytes(args))

    def write_data(self, buf):
        self.i2c.writeto_mem(self.addr, 0x40, buf)

    def fill(self, col):
        self.framebuf.fill(col)

    def pixel(self, x, y, col):
        self.framebuf.pixel(x, y, col)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, col=1):
        self.framebuf.text(string, x, y, col)

    def line(self, x1, y1, x2, y2, col):
        self.framebuf.line(x1, y1, x2, y2, col)

    def hline(self, x, y, w, col):
        self.framebuf.hline(x, y, w, col)

    def vline(self, x, y, h, col):
        self.framebuf.vline(x, y, h, col)

    def rect(self, x, y, w, h, col):
        self.framebuf.rect(x, y, w, h, col)

    def fill_rect(self, x, y, w, h, col):
        self.framebuf.fill_rect(x, y, w, h, col)

    def show(self):
        for page in range(self.pages):
            self.write_cmd(0xB0 + page, 0x02, 0x10)
            self.write_data(self.buffer[page * self.width:(page + 1) * self.width])

class SH1106_I2C(SH1106):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__(width, height, i2c, addr, external_vcc)

    def write_cmd(self, *args):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        for arg in args:
            self.temp[1] = arg
            self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        hdr = bytearray(1)
        hdr[0] = self.addr << 1
        self.i2c.start()
        self.i2c.write(hdr)
        self.i2c.write(bytearray([0x40]))  # Co=0, D/C#=1
        self.i2c.write(buf)
        self.i2c.stop()