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
yellow = (255, 255, 0)
green = (0, 206, 44)
lightGreen = (0, 249, 54)
blue = (5, 0, 165)
lightBlue = (8, 0, 255)



def introscreen():
    """Displays the intro screen
    Made up of a background, buttons and text

    Args:
        arg1: none

    Returns:
        description of the stuff that is returned by the function.

    Raises:
        AnError: An error occurred running this function.
    """
    screen.fill(white) #fills the screen with a background colour
    button("PLAY",50,500,150,50,green,lightGreen,34,"play")
    button("INSTRUCTIONS",300,500,200,50,blue,lightBlue,34,"instructions")
    button("QUIT",600,500,150,50,red,lightRed,34,"quit")
    rTxt("Racing to the end of the universe",400,50,48)
    
    


    pass

def button(txt,x,y,l,h,colour,Hcolour,txtSize,action = None):
    """Creates buttons and makes them interactive
    Takes arguments and creates buttons to be displayed on the pygame screen, mouse position is then check to see if a button is highlighted or clicked.
    Once clicked it will be sent to a different subroutine

    Args:
        txt: text to be displayed within the button
        x: x value the button will be placed
        y: y value the button will be placed
        l: length of the button
        h: height of the button
        colour: natural colour displayed on the screen
        Hcolour: colour displayed when the button is highlighted
        txtSize: size of text in the button

    Returns:

    Raises:
        AnError: An error occurred running this function.
    """
    mouse= P.mouse.get_pos() #gets X and Y of mouse position
    click= P.mouse.get_pressed() #gets postion of mouse when clicked
    
    if x+l>mouse[0]>x and y+h>mouse[1]>y: #asks if the mouse is in the region where the button is located.
        P.draw.rect(screen,Hcolour,(x,y,l,h)) #draws a rectangle with the highlighted colour if mouse is on it
        if click[0]==1 and action!=None: #asks if the button has been clicked when it is within the reigion and if action is doing nothing
            if action=="play": #determines which action to fufil
                print('play button was clicked')
            elif action =="instructions":
                print('instruction button was clicked')
            elif action =="quit":
                P.quit()
                quit()
    else:
        P.draw.rect(screen,colour,(x,y,l,h)) #draws a rectangle with the normal colour if mouse isnt on it
    x1,y1 = ((x+(l/2)),(y+(h/2))) #sets coordinates for text using the length and height of the button as this cannot be done inside the Rtxt module
    rTxt(txt,x1,y1,txtSize) #referes to the rTxt module to render the text inside the button
    
            
    
    pass

def rTxt(msg,x,y,size):
    """Renders and blits text
    This module will be used whenever you would like to render text into the pygame window

    Args:
        msg: text to be displayed
        x: x value the button will be placed
        y: y value the button will be placed
        l: length of the button
        h: height of the button
        size: size of text

    Returns:
        description of the stuff that is returned by the function.

    Raises:
        AnError: An error occurred running this function.
    """
    
    font = P.font.SysFont("comic sans",size) #creates a font for the render function to use
    text = font.render(msg,True,black) #creates a text for the blit function to use
    x,y = ((x- (text.get_rect().w/2)),(y- (text.get_rect().h/2))) #centres the text depening on the length and height of the text
    screen.blit(text,(x,y))
    
    
play = True   
# game loop - runs loopRate times a second!
while play:  # game loop - note:  everything in this loop is indented one tab

    for event in P.event.get():  # get user interaction events
        if event.type == P.QUIT:  # tests if window's X (close) has been clicked
            play = False  # causes exit of game loop
        
        # your code starts here #
        introscreen() #displays the intro screen

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


