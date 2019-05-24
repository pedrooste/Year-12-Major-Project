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

#creates objects to be used later on in arrowButton class
leftB = arrowButton(yellow,lightYellow,150,50,"left")
rightB = arrowButton(yellow,lightYellow,150,50,"right")


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
    #draws the play, quit and instruction button
    playScreen = playB.draw(screen,50,500, playScreen) 
    playScreen =quitB.draw(screen,600,500, playScreen)
    playScreen =instructionsB.draw(screen,300,500, playScreen)
    return playScreen

def playGame(playScreen):
    """Displays the game screen
    this will then reference to other classes

    Args:
        playScreen: determines which screen to be displayed
    Returns:
        playScreen: determines which screen to be displayed

    Raises:
        AnError: An error occurred running this function.
    """
    screen.fill(grey) #fills the screen with a background colour
    playScreen = introB.draw(screen,600,50,playScreen) #draws the back button which only will be used to go back to the intro screen
    leftB.arrowDraw(screen,50,500)
    rightB.arrowDraw(screen,600,500)

    return playScreen

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
    playScreen = introB.draw(screen,600,500, playScreen)

    return playScreen

play = True
playScreen = "intro" #intialises what screen to start on
# game loop - runs loopRate times a second!
while play:  # game loop - note:  everything in this loop is indented one tab

    for event in P.event.get():  # get user interaction events
        if event.type == P.QUIT:  # tests if window's X (close) has been clicked
            play = False  # causes exit of game loop
        
        if playScreen == "intro": #this checks what screen to display by using a variable called playScreen
            playScreen = introscreen(playScreen) #displays the intro screen
        elif playScreen == "play":
            playScreen = playGame(playScreen) #displays the play screen
        elif playScreen == "instructions":
            playScreen = instructionScreen(playScreen) #displays the instructions screen
            
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


