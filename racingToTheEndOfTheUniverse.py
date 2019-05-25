""" Racing to the end of the universe!
A simple car game involving pygame. You control a car on a road in which you have to dodge oncomming cars, this will get harder as the game progresses.
"""

__author__ = "Pedro Oste"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "Pedro.oste@education.nsw.com.au"
__status__ = "Alpha"

#dependencies
import pygame as P # accesses pygame files
import sys  # to communicate with windows
from mods import *


# pygame setup - only runs once
P.init()  # starts the game engine
clock = P.time.Clock()  # creates clock to limit frames per second
loopRate = 60  # sets max speed of main loop
SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 800, 600  # sets size of screen/window
screen = P.display.set_mode(SCREENSIZE)  # creates window and game screen
P.display.set_caption("Racing to the end of the universe!") #sets the game window caption

# set variables for some colours if you wnat them RGB (0-255)
white = (255, 255, 255)
black = (0, 0, 0)
red = (216, 0, 0)
lightRed = (255, 0, 0)
yellow = (234, 226, 0)
lightYellow = (255,255,0)
green = (0, 206, 44)
lightGreen = (0, 249, 54)
blue = (5, 0, 165)
lightBlue = (8, 0, 255)
grey = (92, 98, 112)

#creates objects to be used later on in button class
playB = button(green,lightGreen,150,50,"PLAY",34,black,"play")
quitB = button(red,lightRed,150,50,"QUIT",34,black,"quit")
instructionsB = button(blue,lightBlue,200,50,"INSTRUCTIONS",34,black,"instructions")
introB = button(red,lightRed,150,50,"BACK",34,black,"intro")
mainMenuB = button(red,lightRed,200,50,"MAIN MENU",34,black,'mainMenu')

#creates objects to be used later on in arrowButton class
leftB = arrowButton(yellow,lightYellow,100,50,"left")
rightB = arrowButton(yellow,lightYellow,100,50,"right")

#creates objects to be used later in player class
mcar = player(red,green,50,50) #main player car

#creates initial variables that will be used
carX = 375 #x cordinate for car
play = True
playScreen = "intro" #intialises what screen to start on

def introscreen(playScreen):
    """Displays the intro screen
    Made up of a background, buttons and text

    Args:
        playScreen: determines which screen to be displayed

    Returns:
        playScreen: determines which screen to be displayed

    Raises:
        AnError: An error occurred running this function.
    """
    screen.fill(white) #fills the screen with a background colour
    rTxt(screen,"Racing to the end of the universe",400,50,48,black)
    #draws the play, quit and instruction button
    playScreen = playB.draw(screen,50,500, playScreen) 
    playScreen =quitB.draw(screen,600,500, playScreen)
    playScreen =instructionsB.draw(screen,300,500, playScreen)
    return playScreen

def playGame(playScreen,carX):
    """Displays the game screen
    this will then reference to other classes

    Args:
        playScreen: determines which screen to be displayed
    Returns:
        playScreen: determines which screen to be displayed

    Raises:
        AnError: An error occurred running this function.
    """
    screen.fill(grey) #fills the screen with a background colour , has to be placed first
    #while these lines are inconvient now, a class will be made to draw and update the background once graphics are introduced
    P.draw.line(screen,white,[100,0],[100,600],5)
    P.draw.line(screen,white,[700,0],[700,600],5)
    
    oldCarX = carX #creates a temporary variable which will be checked later on to see if the x postion has been changed
    
    playScreen = introB.draw(screen,600,50,playScreen) #draws the back button which only will be used to go back to the intro screen
    carX = leftB.draw(screen,50,500,carX)
    carX = rightB.draw(screen,650,500,carX)
    
    if oldCarX == carX: #if the x postion has been changed then movement will be true. If movement is true then the rectangle will be draw a different colour
        movement = False
    else:
        movement = True
        
    mcar.draw(screen,carX,500,movement) #draws the rectangle car
    
    if carX>600+50 or carX<100: #creates a boundry that the car must stay in, however these numbers will be changed when graphics are implemented (based off drawn lines)
        playScreen = "crash"

    return playScreen, carX #need to return the playScreen so we know what screen we are on and the carX so we know were to start from when the loop is redone.

def instructionScreen(playScreen):
    """Displays the instructions screen
    this will then reference to other classes

    Args:
        playScreen: determines which screen to be displayed
    Returns:
        playScreen: determines which screen to be displayed

    Raises:
        AnError: An error occurred running this function.
    """
    screen.fill(black) #fills the screen with a background colour
    rTxt(screen,"Instructions",400,50,48,white)
    playScreen = introB.draw(screen,600,500, playScreen) #draws the back button for the intro screen

    return playScreen

def crashScreen(playScreen,carX):
    """Displays the crash screen when a boundry is met
    this will reference to other classes and modules to display a screen

    Args:
        
    Returns:
        
    Raises:
        
    """
    P.draw.rect(screen,white,(100,50,600,500))
    rTxt(screen,"You crashed",400,100,48,black)
    playScreen = mainMenuB.draw(screen,300,450,playScreen)
    if playScreen == "intro":
        carX = 375
    
    return playScreen,carX

# game loop - runs loopRate times a second!
while play:  # game loop - note:  everything in this loop is indented one tab

    for event in P.event.get():  # get user interaction events
        if event.type == P.QUIT:  # tests if window's X (close) has been clicked
            play = False  # causes exit of game loop
        
        if playScreen == "intro": #this checks what screen to display by using a variable called playScreen
            playScreen = introscreen(playScreen) #displays the intro screen
        elif playScreen == "play":
            playScreen,carX = playGame(playScreen,carX) #displays the play screen
        elif playScreen == "instructions":
            playScreen = instructionScreen(playScreen) #displays the instructions screen
        elif playScreen == "crash":
            playScreen,carX = crashScreen(playScreen,carX)
            
        else:
            playScreen = "intro"
            print("there has been an error with playScreen, reverted to intro")

        if event.type == P.MOUSEBUTTONDOWN: #includes touching screen
            # change this to do something if user clicks mouse
            # or touches screen
            pass 
        


    # your code ends here #
    P.display.flip()  # makes any changes visible on the screen
    clock.tick(loopRate)  # limits game to frame per second, FPS value

# out of game loop #
print("Thanks for playing")  # notifies user the game has ended
P.quit()   # stops the game engine
sys.exit()  # close operating system window


