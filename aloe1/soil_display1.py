from machine import ADC, Pin
from utime import sleep
#import picographics
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
import jpegdec

moisture = ADC(26)
#for usage with round screen
#display = picographics.PicoGraphics(display=picographics.DISPLAY_ROUND_LCD_240X240)
#for usage with PICO Display rectangle
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY) #rotate=0 will turn on side

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)

def loadimage(filename):
# Create a new JPEG decoder for our PicoGraphics
    j = jpegdec.JPEG(display)
    print("about to load image file")
# Open the JPEG file
    j.open_file(filename)
# Decode the JPEG
    j.decode(5, 0, jpegdec.JPEG_SCALE_FULL)
    print("about to update display with " + filename)
# Display the result
    display.update()
    return 1


while True:
    # fills the screen with black
    display.set_pen(BLACK)
    display.clear()

    reading = moisture.read_u16()
    voltage = 3300 * reading/65535
    print("{:.1f}mV".format(voltage))
    display.set_pen(WHITE)
    display.set_font("bitmap8")
    display.text("{:.1f}mV".format(voltage), 20, 150, scale=3)
#    display.update()
    
    if voltage < 15:
        imageface = "sadface.jpg"
    elif voltage > 30:
        imageface = "drownface.jpg"
    else:
        imageface = "tony.jpg"
    success = loadimage(imageface)
#    print(success)
    sleep(2)

#<15 seems to be very wet
#30 seems to be fresh air / bone dry
#from that we can work out some trigger rules
    
