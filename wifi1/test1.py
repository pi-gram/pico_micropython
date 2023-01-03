from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from jpegdec import JPEG

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)

WHITE = display.create_pen(255, 255, 255)
display.set_pen(WHITE)
display.set_font('bitmap8')
display.text("Hello   Tony", 0, 0, 320, 4)
display.update()

j = JPEG(display)
j.open_file("tony.jpg")
j.decode()
display.update()
