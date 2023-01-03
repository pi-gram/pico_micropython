from time import sleep
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
import random

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8, rotate=180) #ah! this moved it all sideways!
display.set_backlight(0.5)
display.set_font("serif") #bitmap6, bitmap8, bitmap14_outline
# sans, serif, cursive, gothic=vector, so can change angle

buttonA = Button(12) #SCORE
buttonB = Button(13) #FIRE
right   = Button(14) #RIGHT
left    = Button(15) #LEFT

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
#RED = display.create_pen()

WIDTH, HEIGHT = display.get_bounds()

#initialise game variables to default values
invader         = ""
ship            = ""
ufo             = ""
spritex         = 5
spritey         = 5
invadercountx   = 4
invadercounty   = 5
invaderspacingx = 7
invaderspacingy = 5
invader_colour  = WHITE
#######################
addy            = 12 #number of pixels of movement sideways per turn on invaders (in future make faster when difficulty is higher)
loopCount       = 0
score           = 0
difficulty      = 1
showufo         = False
ufoy            = 0
ufoCount        = 0
shippos         = 30
shipmid         = 25
shotx           = 250               #set to off screen / default value
shoty           = shippos + shipmid #shippos will vary as ship moves left/right on screen
missile_speed   = 4                 #set to 2 for slower missiles, set to 4 for faster - could add to button_A press to increase?
#######################
invaders        = []

class Invader(object):
    
    def __init__(self, type, x, y):
        self.visible = True
        self.type = type
        self.x = x
        self.y = y
        self.origx = x
        self.origy = y
    
def create_invader(type, x, y):
    invader = Invader(type, x, y)
    return invader

def define_invaders():
    type = "invader" 
    for x in range (1, invadercountx + 1):
        for y in range (1, invadercounty + 1):
            invaders.append(create_invader(type, (210 - ((x * (spritex + invaderspacingx)) - spritex)), (y * (spritey + invaderspacingy)) - spritey))

#used to reset invaders to starting position and optionally visibility
def reset_invaders(visibility): 
    x = 1
    y = 1
    for c in invaders:
        if visibility:
            c.visible = True
        c.x = c.origx
        c.y = c.origy
            
def draw_invader(invader_type, pen, x, y):
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
    new_x = x;
    new_y = y+15; #15
    #want to change this to a triangle
    display.set_pen(BLACK)
    display.rectangle(cur_x, cur_y, 20, 20)
    display.set_pen(pen)
    display.rectangle(new_x, new_y, 20, 20)

def draw_ufo(ufo_type, pen, x, y):
    cur_x = x;
    cur_y = y;
    new_x = x;
    new_y = y+15; #20
    display.set_pen(BLACK)
    display.rectangle(cur_x, cur_y, 10, 20)
    display.set_pen(pen)
    display.rectangle(new_x, new_y, 10, 20)
    
#sets up a handy function we can call to clear the screen
#do not use inbetween calls to .update as will cause too many refreshes
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()


#main intialisation steps when code executes


#remove any previous items left on the screen
clear()
#showsplashscreen()
#show the SPLASH SCREEN
sleep(1)
#now clear the display ready for user input - we should wait until pressing button_a?
clear()
sleep(1)


#initialise and create the invaders
define_invaders()


#main game loop
while True:
    
    # 1 in 350 chance of running this loop that UFO will appear
    ufoChance = random.randrange(1, 350, 1) 
    if ufoChance == 123 and showufo == False:
        showufo = True
        ufoy = 0
    if showufo:
        ufoy = ufoy + 1
        #if near edge of screen then do not show
        if ufoy > 120:
            ufoy = 0
            showufo = False
    loopCount = loopCount + 1
    
    #do not make a call to clear() as that will do an extra .update() call and too many refreshes happen
    display.set_pen(BLACK)
    display.clear()
    
    #exceute the following when invaders have reached edge of screen
    if loopCount > 16 - difficulty:         
        dropdown = False
        loopCount = 0             #reset loopCounter
        for c in invaders:
            if c.visible == True: #check if need to move invaders
                if c.y + addy > 125 or c.y + addy < 1: #are any of the visible invaders at the edge of the screen?
                    if c.x - 3 < 90:                   #if invaders are at the bottom by the ship, reset position to the top
                        reset_invaders(False)
                        dropdown = False
                    dropdown = True

        if dropdown == True:   #move the invaders down if any of the visible ones hit the screen edge
            addy = addy * -1
            for c in invaders:
                c.x = c.x - 12 #number of pixels to move the invaders downwards
        else:
            for c in invaders:
                c.y = c.y + addy
                
    if left.read():
        if shippos > 1:
            shippos = shippos - 3  #how many pixels to move left
    
    if right.read():
        if shippos < 100:
            shippos = shippos + 3  #how many pixels to move right

    shotx = shotx + missile_speed  #this moves the missile towards the invaders, low=slower, higher=faster
    
    foundVisible = False #By default, assume all the invaders are dead
    
    #if showing the ufo, need to do see if we have hit it with the missile
    if showufo:
        if shotx > 210 and shotx < 240:     #only interested if the missile is in the top region is the screen
#            print("shoty:"+str(shoty)+" ufoy:"+str(ufoy))
            if shoty >= ufoy:
                if shoty < ufoy + 20: #12            
                    #could draw an indicator that it was hit? maybe in RED?
                    #does flash slightly to indicate it was hit
                    draw_ufo(ufo, WHITE, 220, ufoy)
                    score   = score + 50
                    showufo = False
                    ufoy    = 0
                    #reset the missle
                    shotx   = 250               #set to off screen / default value
                    shoty   = shippos + shipmid #set so missile fires from middle of ship
                    
    #loop through all invaders and detect if we have been hit by the missile
    for c in invaders:
        if shotx >= c.x and c.visible == True:
            if shotx - 4 <= c.x + 8:        #tweak these for better detection?
                if shoty > c.y:
                    if shoty <= c.y + 10:   #we hit an invader!   #was 7
                        c.visible = False   #hide the invader
                        score = score + 10
                        #reset the missile
                        shotx = 250               #set to off screen / default value
                        shoty = shippos + shipmid #set so missile fires from middle of ship
                        
        #if visible then drw invader to screen
        if c.visible == True:
            foundVisible = True
            draw_invader(invader, invader_colour, c.x, c.y)

        #if visible then draw the ufo to screen
        if showufo:
            draw_ufo(ufo, MAGENTA, 220, ufoy)

    #if missile is off the screen then allow button press to fire another one
    if shotx > 240:
        if buttonB.read():
            shotx = 40
            shoty = shippos + shipmid #set so missile fires from middle of ship
        else:
            shotx = 250 #need to valid this?
  
    #if all invaders shot, then finished the level, increase difficulty level and reset invaders
    if foundVisible == False:
            if difficulty < 10:
                difficulty = difficulty + 1
            reset_invaders(True)
    
    # draw the ship (prefer to be a triangle)
    draw_ship(ship, YELLOW, 18, int(shippos)) 
    
    #draw the missile (shame cannot change thickness)
    #the -4 is the length of the missile
    display.line(shotx, shoty, shotx - 4, shoty) 
 
    #allow to speed up missle firing speed - but only so far!
    if buttonA.read():
        missile_speed = missile_speed + 1
        if missile_speed == 10:
            missile_speed = 2

    #I believe showing text slows down the UI quite a bit
#    display.set_pen(invader_colour)
#    display.text("["+str(difficulty)+"] score:"+str(score), 8, 5, angle=90, scale=0.5)

    #depending upon the difficulty level change the invader colours
    if difficulty == 1:
        invader_colour = WHITE
    elif difficulty == 2:
        invader_colour = YELLOW
    elif difficulty == 3:
        invader_colour = MAGENTA
    else:
        invader_colour = WHITE
                  
    #update all screen shapes in one go
    display.update()
    
    #wait for a very small period of time before doing it all again
    sleep(0.001)
        