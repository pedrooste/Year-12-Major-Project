""" Racing to the end of the universe!
A simple car game involving pygame. You control a car on a road in which you have to dodge oncomming cars, this will get harder as the game progresses.
"""

__author__ = "Pedro Oste"
__license__ = "GPL"
__version__ = "1.0.2"
__email__ = "Pedro.oste@education.nsw.com.au"
__status__ = "Alpha"

#dependencies
import pygame as P # accesses pygame files
import sys  # to communicate with windows
import random as R #import the random function
from mods import *


# pygame setup - only runs once
P.init()  # starts the game engine
clock = P.time.Clock()  # creates clock to limit frames per second
loopRate = 60  # sets max speed of main loop
SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 800, 600  # sets size of screen/window
screen = P.display.set_mode(SCREENSIZE)  # creates window and game screen
P.display.set_caption("Racing to the end of the universe!") #sets the game window caption

# set variables for some colours if you want them RGB (0-255)
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

#creates the enemy cars to be used later on
Ecar1 = Ecar(white,5,25,25)

#creates initial variables that will be used
carX = 375 #x cordinate for car
play = True #controls main loop
playScreen = "intro" #intialises what screen to start on
score = 0 #initialises score because theres no headstarts here

def introscreen(playScreen):
    """Displays the intro screen
    Made up of a background, buttons and text

    Args:
        playScreen: determines which screen to be displayed

    Returns:
        playScreen: determines which screen to be displayed

    Raises:

    """
    screen.fill(white) #fills the screen with a background colour
    rTxt(screen,"Racing to the end of the universe",400,50,48,black)
    #draws the play, quit and instruction button
    playScreen = playB.draw(screen,50,500, playScreen) 
    playScreen =quitB.draw(screen,600,500, playScreen)
    playScreen =instructionsB.draw(screen,300,500, playScreen)
    return playScreen

def playGame(playScreen,carX,score):
    """Displays the game screen
    this will then reference to other classes

    Args:
        playScreen: determines which screen to be displayed
        carX: current postion of the x coordinate of the car
    Returns:
        playScreen: determines which screen to be displayed
        carX: current postion of the x coordinate of the car (to be referenced to when the game loop restarts

    Raises:

    """
    screen.fill(grey) #fills the screen with a background colour , has to be placed first
    #while these lines are inconvient now, a class will be made to draw and update the background once graphics are introduced
    P.draw.line(screen,white,[100,0],[100,600],5)
    P.draw.line(screen,white,[700,0],[700,600],5)
    
    oldCarX = carX #creates a temporary variable which will be checked later on to see if the x postion has been changed
    #draws left and right buttons
    carX = leftB.draw(screen,50,500,carX)
    carX = rightB.draw(screen,650,500,carX)
    
    if oldCarX == carX: #if the x postion has been changed then movement will be true. If movement is true then the rectangle will be draw a different colour
        movement = False
    else:
        movement = True
    
    score = Ecar1.draw(screen,score) #draws the enemy car    
    mcar.draw(screen,carX,movement) #draws the main player rectangle car
    



    rTxt(screen,("Score: "+str(score)),100,50,48,black)    
    playScreen = introB.draw(screen,600,50,playScreen) #draws the back button which only will be used to go back to the intro screen
    
    crash = Ecar1.checkHit(carX) #checks if the car hits the enemy car
    if crash == True:
        playScreen = "crash" #sends to crash screen
    if carX>600+50 or carX<100: #creates a boundry that the car must stay in, however these numbers will be changed when graphics are implemented (based off drawn lines)
        playScreen = "crash"

    return playScreen, carX, score#need to return the playScreen so we know what screen we are on and the carX so we know were to start from when the loop is redone.
                                  # also need to pass score to keep track of the score

def instructionScreen(playScreen):
    """Displays the instructions screen
    this will then reference to other classes

    Args:
        playScreen: determines which screen to be displayed
    Returns:
        playScreen: determines which screen to be displayed

    Raises:

    """
    screen.fill(black) #fills the screen with a background colour
    rTxt(screen,"Instructions",400,50,48,white)
    playScreen = introB.draw(screen,600,500, playScreen) #draws the back button for the intro screen

    return playScreen

def crashScreen(playScreen,carX,score):
    """Displays the crash screen when a boundry is met
    this will reference to other classes and modules to display a screen

    Args:
        playScreen: determines which screen to be displayed
        carX: determines position of car (this is sent so it can be reset if intro button is clicked)
    Returns:
        playScreen: determines which screen to be displayed
        carX: determines position of car (reset version)
    Raises:
        
    """

    P.draw.rect(screen,white,(100,50,600,500)) #draws background screen
    rTxt(screen,"You crashed!",400,100,48,black) #displays text saying you crashed
    rTxt(screen,("Score: "+str(score)),400,200,48,black) #displays your score
    playScreen = mainMenuB.draw(screen,300,450,playScreen) #draws a main menu button

    if playScreen == "intro": #if the palyer wants to go to the main menu, positions must be reset
        carX = 375 #car reset positon
        score = 0 # resets the score
        Ecar1.reset() #calls class method to reset the value of the coordinates for each object
    
    return playScreen,carX, score

# game loop - runs loopRate times a second!
while play:  # game loop - note:  everything in this loop is indented one tab

            
    if playScreen == "intro": #this checks what screen to display by using a variable called playScreen
        playScreen = introscreen(playScreen) #displays the intro screen
    elif playScreen == "play":
        playScreen,carX,score = playGame(playScreen,carX,score) #displays the play screen
    elif playScreen == "instructions":
        playScreen = instructionScreen(playScreen) #displays the instructions screen
    elif playScreen == "crash":
        playScreen,carX,score = crashScreen(playScreen,carX,score)
            
    else:
        playScreen = "intro"
        print("there has been an error with playScreen, reverted to intro")
        
    for event in P.event.get():  # get user interaction events
        if event.type == P.QUIT:  # tests if window's X (close) has been clicked
            play = False  # causes exit of game loop

        
    # your code ends here #
    P.display.flip()  # makes any changes visible on the screen
    clock.tick(loopRate)  # limits game to frame per second, FPS value

# out of game loop #
print("Thanks for playing")  # notifies user the game has ended
P.quit()   # stops the game engine
sys.exit()  # close operating system window


