import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=270)  #0, 90, 180 and 270 degree rotations
#270 is correct orientation for upright display
#1-bit - PEN_1BIT - mono, used for Pico Inky Pack and i2c OLED
#3-bit - PEN_3BIT - 8-colour, used for Inky Frame
#4-bit - PEN_P4   - 16-colour palette of your choice
#8-bit - PEN_P8   - 256-colour palette of your choice

display.set_backlight(0.5)
display.set_font("bitmap6") #bitmap6, bitmap8, bitmap14_outline

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)

WIDTH, HEIGHT = display.get_bounds()

#set global values
ship_sx = 20
ship_sy = 220
missile_fired = 0

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()

# now clear the screen
clear()

def button_Y(): #do action for button Y (LEFT)
#    clear()
    display.set_pen(YELLOW)
    display.text("<<<GO LEFT", 10, 10, 135, scale=2)
    display.set_pen(BLACK)
    draw_ship(ship_sx) #blank out ship in current location
    display.set_pen(YELLOW)
    newl_x = ship_sx - 5
    draw_ship(newl_x)  #draw ship in new location
#    display.update()
#    time.sleep(1)
    return newl_x
#    clear()

def button_X(): #do action for button X (RIGHT)
#    clear()
    display.set_pen(MAGENTA)
    display.text("GO RIGHT>>>", 10, 10, 135, scale=2)
    display.set_pen(BLACK)
    draw_ship(ship_sx) #blank out ship in current location
    display.set_pen(MAGENTA)
    newr_x = ship_sx + 5
    draw_ship(newr_x)  #draw ship in new location
    return newr_x
#    clear()

def button_A():
    clear()                                           # clear to black
    display.set_pen(WHITE)                            # change the pen colour
    display.text("Button A", 10, 10, 135, scale=2)    # display some text on the screen
    display.update()                                  # update the display
    time.sleep(1)                                     # pause for a sec
    clear()                                           # clear to black again
    
def button_B(): #FIRE missile button
    display.set_pen(CYAN)
    display.text("!FIRE!", 10, 10, 135, scale=2)
    X1 = int(WIDTH / 2)
    #we should get the current location of ship and put this above/middle of co-ords
    draw_missle(X1, 200, X1-10, 210, X1+10, 210)
    return 1
#    time.sleep(1)
#    clear()

def draw_missle(x1, y1, x2, y2, x3, y3):
    display.triangle(x1, y1, x2, y2, x3, y3)
    display.update()

def draw_ship(x1):
    display.rectangle(x1, ship_sy, 20, 20)
    display.update()


while True:
#    draw_ship(ship_sx) #draw ship in current location
#    display.update()
    if button_a.read():                                   # if a button press is detected then...
        button_A()
    elif button_b.read():
        missile_fired = button_B()
    elif button_x.read():
        nrx = button_X()
        print(nrx)
        ship_sx = nrx
    elif button_y.read():
        nlx = button_Y()
        print(nlx)
        ship_sx = nlx
    else:
        #if no buttons are pressed then just move the aliens
        #and move the missile upwards 1 block further
        #check if missle has collided with alien, if yes, set alien to BLACK and make inactive
#        display.set_pen(GREEN)
#        display.text("Press button", 220, 10, 135, scale=2)
#        draw_ship(ship_sx) #draw ship in current location
#        display.update()
        if (missile_fired == 1):
            print('keep moving missile upwards');
        time.sleep(0.1)  # this number is how frequently the Pico checks for button presses

#text fonts
#    sans, gothic, cursive, serif_italic, serif
 
#display.text(text, x, y, wordwrap, scale, angle, spacing)

#display.triangle(x1, y1, x2, y2, x3, y3)
#display.rectangle(x, y, w, h)
#display.circle(x, y, r)
#display.line(x1, y1, x2, y2)
#display.polygon([
#  (0, 10),
#  (20, 10),
#  (20, 0),
#  (30, 20),
#  (20, 30),
#  (20, 20),
#  (0, 20),
#])
#display.pixel(x, y)  #draw individual pixel
#pixel_span(x, y, length) #draw horizontal span of pixels faster (let's say 10 at once) shame it's not vertical!

