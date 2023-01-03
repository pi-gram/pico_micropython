from time import sleep
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
import random

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=180) #ah! this moved it all sideways!
display.set_backlight(0.5)
display.set_font("bitmap6") #bitmap6, bitmap8, bitmap14_outline

#button_a = Button(12)
button1 = Button(13) #FIRE
right = Button(14) #RIGHT
left = Button(15) #LEFT

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)

WIDTH, HEIGHT = display.get_bounds()

inv1a = ""
inv1aBuff = ""
inv1b = ""
inv1bBuff = ""
inv2a = ""
inv2aBuff = ""
inv2b = ""
inv2bBuff = ""
ship = ""
shipBuff = ""
ufo = ""
ufoBuff = ""
spritex = 5
spritey = 5
aliencountx = 4
aliencounty = 5
alienspacingx = 7
alienspacingy = 5
alien_colours = WHITE

aliens = []
class Alien(object):
    
    def __init__(self, type, x, y):
        self.visible = True
        self.type = type
        self.x = x
        self.y = y
        self.origx = x
        self.origy = y
    
def create_alien(type, x, y):
    alien = Alien(type, x, y)
    return alien

def define_aliens():
    type = "inv1a" #First row is type 1. 
    for x in range (1, aliencountx + 1):
        for y in range (1, aliencounty + 1):
            aliens.append(create_alien(type, (210 - ((x * (spritex + alienspacingx)) - spritex)), (y * (spritey + alienspacingy)) - spritey))
#        if type == "inv1a":
#            type = "inv2a" #Second row is type 2
#        else:
#            type = "inv1a"

def reset_aliens(visibility): # Used to reset aliens to starting position and, optionally, visibility
    x = 1
    y = 1
    for c in aliens:
        if visibility:
            c.visible = True
            
        c.x = c.origx
        c.y = c.origy
            
def draw_alien(alien_type, pen, x, y):
    cur_x = x;
    cur_y = y;
    new_x = x+10;
    new_y = y+0;
    display.set_pen(BLACK)
    display.circle(cur_x,cur_y,5) #x,y,radius
    display.set_pen(pen)
    display.circle(new_x,new_y,5) #x,y,radius
    

def draw_ship(ship_type, pen, x, y):
    cur_x = x;
    cur_y = y;
    new_x = x+15;
    new_y = y+0;
    display.set_pen(BLACK)
    display.rectangle(cur_x, cur_y, 20, 20)
    display.set_pen(pen)
    display.rectangle(new_x, new_y, 20, 20)

def draw_ufo(ufo_type, pen, x, y):
    cur_x = x;
    cur_y = y;
    new_x = x;
    new_y = y+20;
    display.set_pen(BLACK)
    display.rectangle(cur_x, cur_y, 10, 20)
    display.set_pen(pen)
    display.rectangle(new_x, new_y, 10, 20)
    

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()

#clear the display
clear()
sleep(1)

addy = 12 #3 #pixels of movement sideways per turn on aliens, future make faster when difficulty is higher

shotx = 1
shoty = 250
loopCount = 0
define_aliens()
score = 0
difficulty = 1
showufo = False
ufoy = 0
ufoCount = 0
shippos = 30

while True:
    ufoChance = random.randrange(1, 350, 1) # 1 in 1000 chance of running this loop that UFO will appear
    if ufoChance == 123 and showufo == False:
        showufo = True
        ufoy = 0
    if showufo:
        ufoy = ufoy + 1
        if ufoy > 120:
            showufo = False
    loopCount = loopCount + 1
#    clear() #do we need to do that here? - yes, but it does create horrid refresh rate flash
    display.set_pen(BLACK)
    display.clear()
    #lets eave out the update to see if the refresh is better? - yes, yes, it is!
    if loopCount > 16 - difficulty:         
        dropdown = False
        loopCount = 0
        for c in aliens:
            if c.visible == True: #switch between sprites to animate aliens (shows moving legs = todo)
#not used                
#                if c.type == "inv1a": c.type = "inv1b"
#                elif c.type == "inv1b": c.type = "inv1a"
#                elif c.type == "inv2a": c.type = "inv2b"
#                elif c.type =="inv2b": c.type = "inv2a"
                if c.y + addy > 125 or c.y + addy < 1: #are any of the visible invaders at the edge of the screen?
                    if c.x - 3 < 60: #If they're at the bottom, reset their position
                        reset_aliens(False)
                        dropdown = False
                    dropdown = True
        if dropdown == True: #move the aliens down if any of the visible ones hit the screen edge
            addy = addy * -1
            for c in aliens:
                c.x = c.x - 12 #3 how many pixels to move the aliens downwards
        else:
            for c in aliens:
                c.y = c.y + addy
                
    if left.read():
        if shippos > 1:
            shippos = shippos - 1
    
    if right.read():
        if shippos < 100:
            shippos = shippos + 1

    shotx = shotx + 2
#    print(shotx)
#    print(shoty)
    foundVisible = False #By default, assume all the aliens are dead
    if showufo:
        if shotx > 180 and shotx < 240:
            if shoty >= ufoy:
                if shoty < ufoy + 12:       #need to examine this as never seems to work?
                    score = score + 50
                    showufo = False
                    ufoy = 0
                    shotx = 250
                    shoty = int(shippos) + 6
                    
    for c in aliens:
        if shotx >= c.x and c.visible == True: #Collision detection for aliens with the shots
            #this currently sucks! need to make it a little bit wider
            if shotx - 4 <= c.x + 8:        #increase variable here, but not too much
                if shoty > c.y:
                    if shoty <= c.y + 7: #You hit an alien!
                        c.visible = False 
                        score = score + 10
                        shotx = 250
                        shoty = int(shippos) + 6
        if c.visible == True:
            foundVisible = True
            if c.type == "inv1a": #Display aliens
                draw_alien(inv1aBuff, alien_colours, c.x, c.y)
            elif c.type == "inv1b":
                draw_alien(inv1bBuff, alien_colours, c.x, c.y) #display animation frame 2, set to frame 1 for next time
            elif c.type == "inv2a":
                draw_alien(inv2aBuff, alien_colours, c.x, c.y) #display animation frame 1, set to frame 2 for next time
            elif c.type == "inv2b":
                draw_alien(inv2bBuff, alien_colours, c.x, c.y) #display animation frame 2, set to frame 1 for next time
        if showufo:
            draw_ufo(ufoBuff, MAGENTA, 220, ufoy)
            
    if shotx > 240:
        if button1.read():
            shotx = 32
            shoty = int(shippos) + 6
        else:
            shotx = 250
  
    if foundVisible == False: # You finish the level! Increase the difficulty and reset the aliens
            if difficulty < 10:
                difficulty = difficulty + 1
            reset_aliens(True)
    
    draw_ship(shipBuff, YELLOW, 18, int(shippos)) # draw the ship (prefer to be a triangle)
    
    display.line(shotx, shoty, shotx - 4, shoty) #draw the missile (shamme cannot change thickness)
        
#    print("score:"+str(score))
#        display.set_pen(MAGENTA)
#        display.text("Score:", 10, 10, 240, 4)
    
#    print("level:"+str(difficulty))
    if difficulty == 1:
        alien_colours = WHITE
    elif difficulty == 2:
        alien_colours = YELLOW
    elif difficulty == 3:
        alien_colours = MAGENTA
    else:
        alien_colours = WHITE            
#        display.set_pen(MAGENTA)
#        display.text("Level:", 10, 10, 240, 4)
                  
    display.update() #update all screen shapes in one go
    
    sleep(0.001)
        