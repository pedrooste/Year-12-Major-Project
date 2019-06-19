""" Racing to the end of the universe!
A simple car game involving pygame. You control a car on a road in which you have to dodge oncomming cars, this will get harder as the game progresses.

this is where all of the classes will be stored, modules can be stored here but global variables have to be passed
"""

__author__ = "Pedro Oste"
__license__ = "GPL"
__version__ = "1.0.2"
__email__ = "Pedro.oste@education.nsw.com.au"
__status__ = "Alpha"


""" revision notes:
- Sprint 1:
    Experimentation of design, what works, what doesn’t ?
- Sprint 2:
    Menu screens added
    Basic game development with little graphics
    Playable gamplay
- Sprint 3:
    Added progressive difficult to the game
    Added a score which updates after each car has passed
    Added a variety of enemy cars with different hit boxes
- Sprint 4:
    Highscore board developed
- Sprint 5:
    Graphics introduced for all models
    Finalisation of any details

"""

#import statements for any dependencies
import pygame as P # accesses pygame files
import random as R #import the random function
import time as T #import the time function
import sys  # to communicate with windows

class button():
    """Creates a button with text (if needed)

    Each object will be created with a number of vairables, these are then rendered out if the draw method is called.
    draw method will blit a lighter image if the mouse is in the same position, also checking if clicked.

    Attributes:
        self.bImage: button image
        self.bImageH: highlighted button image
        self.w: width of button image
        self.h: height of button image
        self.txt: text to be displayed inside of rectangle
        self.size: size of text
        self.tColour: colour of text
        self.action: determines what the buttons action is when clicked
        self.screen: screen that the objects will be displayed to
    """
    def __init__ (self,screen,button,hButton,txt,size,tColour,action):
        self.bImage = button
        self.bImageH = hButton
        self.w = P.Surface.get_width(self.bImage) #gets the width
        self.h = P.Surface.get_height(self.bImage) #gets the height
        self.txt = txt
        self.size = size
        self.tColour = tColour
        self.action = action
        self.screen = screen

    def drawNav(self,x,y,playScreen):
        """method that blits an nav button image on the screen, also checking if the mouse is over the image, if it is it will also check for a click."""
        #gets X and Y of mouse position 
        mouse= P.mouse.get_pos()
        
        #Performs seperate operations if the mouse is over the button (drawing lighter button, checking for click)
        if x+self.w>mouse[0]>x and y+self.h>mouse[1]>y:
            self.screen.blit(self.bImageH, (x,y)) #blits the lighter image of the button           
            
            #gets any clicks that the user performs
            for event in P.event.get():
                P.event.get()
                #asks if the user has completed their click (these buttons can not be held down)
                if event.type == P.MOUSEBUTTONUP and self.action!=None:
                    #determines which action to fufil
                    if self.action=="play":
                        playScreen = "play"
                    elif self.action =="instructions":
                        playScreen = "instructions"
                    elif self.action =="intro":
                        playScreen = "intro"
                    elif self.action =="mainMenu":
                        playScreen = "intro"
                    elif self.action =="highscore":
                        playScreen = "highscore"
                    elif self.action == "pause":
                        playScreen = "pause"
                    elif self.action == "save":
                        save = True
                        return save #returns save instead of playScreen
                    elif self.action == "today":
                        press = False
                        return press #returns whether this button was pressed or not
                    elif self.action == "overall":
                        press = True
                        return press
        #if the mouse is not located over the button...            
        else:
            self.screen.blit(self.bImage, (x,y)) #blits the image of the button
        
        #now we draw the text onto the button (first we have to render)
        font = P.font.SysFont('comicsans', self.size)
        text = font.render(self.txt, 1,self.tColour)
        self.screen.blit(text, (x + (self.w/2 - text.get_width()/2), y + (self.h/2 - text.get_height()/2)))
        return playScreen
    
    def drawArrow(self,x,y,carX):
        """method that blits a arrow button on the screen, also checking if the mouse is over the button, if it is it will also check for a click.
            If the button is clicked, the carX variable will be updated (left and right), this differs as the button can be held down and has to return
            a specific value"""
        #gets X and Y pos of mouse, also checking if it is clicked
        mouse= P.mouse.get_pos()
        click= P.mouse.get_pressed()
        
        #performs opererations if the mouse is located over the button
        if x+self.w>mouse[0]>x and y+self.h>mouse[1]>y:
            self.screen.blit(self.bImageH, (x,y)) #blits the image of the highlighted button
            #asks if the button has been clicked
            if click[0]==1 and self.action!=None:
                #determines which action to fulfil
                if self.action =="right":
                    carX +=5 #car x position is updated
                elif self.action =="left":
                    carX -=5
        #if mouse is not over button...
        else:
            self.screen.blit(self.bImage, (x,y)) #blits the image of the button           
        return carX



class player():
    """blits a car image that is controlled by the player (x movements) via previous buttons
    
    Attributes:
        self.screen: screen that the objects will be displayed to
        self.y: y position the image will be displayed
        self.carN: car image when not moving
        self.carL: car image when moving left
        self.carR: car image when moving right
    """

    def __init__(self,screen,carImage,carImageL,carImageR):
        """Inits Player class with variables"""
        self.screen = screen
        self.y = 470
        self.carN = carImage
        self.carL = carImageL
        self.carR = carImageR

    def draw(self,x,movement):
        """method that blits the player onto the screen"""
        #blits specific movements if the car is travelling left, right or straight
        if movement == 'left':
            self.screen.blit(self.carL, (x,self.y))
        elif movement == 'right':
            self.screen.blit(self.carR, (x,self.y))
        else:
            self.screen.blit(self.carN, (x,self.y))

def rTxt(screen,msg,x,y,size,colour):
    """Renders and blits text
    This function will be used whenever you would like to render text into the pygame window .This is not a class as text wouldnt be treated as an object.
    Args:
        screen: pygame screen to be displayed
        msg: text to be displayed
        x: x value the button will be placed
        y: y value the button will be placed
        size: size of text
        colour: colour of text
    Returns:
        none
    Raises:
        none
    """
    
    font = P.font.SysFont("comic sans",size) #creates a font for the render function to use
    text = font.render(msg,True,colour) #creates a text for the blit function to use
    x,y = ((x- (text.get_rect().w/2)),(y- (text.get_rect().h/2))) #centres the text depening on the length and height of the text
    screen.blit(text,(x,y)) #displays the text
    
    

class Ecar():
    """creates objects for the variety of enemy cars
    these cars are displayed and checked if they collide with the player

    

    Attributes:        
        self.screen: screen that the objects will be displayed to
        self.speed: speed that the enemy car will travel
        self.eImage: enemy car image
        self.w: width of enemy car
        self.h: height of enemy car
        self.y: y postion of the car (this is updated)
        self.initialY: initial y postion of the car (used when reseting postions after a crash)
        self.x: x postion of the car which will be random between the road boundry
        self.playerWidth: width of player car
        self.playerHeight: height of player car
    """

    def __init__(self,screen,eImage,speed,y,playerWidth,playerHeight):
        """Inits SampleClass with blah."""
        self.screen = screen
        self.speed = speed
        self.eImage = eImage
        self.w = P.Surface.get_width(self.eImage) #gets the width
        self.h = P.Surface.get_height(self.eImage) #gets the height
        self.y = y
        self.initialY = y
        self.x = R.randrange(120,(680-self.w)) #minus width as the area of the car as it could exceed the boundry
        self.playerWidth = playerWidth
        self.playerHeight = playerHeight

    def draw(self,score):
        """blits the moving enemy car object"""
        #blits the image of the enemy car
        self.screen.blit(self.eImage, (self.x,self.y))
        
        #checks if object is passed, to which it will reset and be shown again
        if self.y > 800:
            self.resetloop()
            score = score + 1 #increments score each time a car is passed
        #otherwise continues to move down the screen
        else:
            self.y = self.y + self.speed

        return score
        
    def checkHit(self,carX):
        """checks if the player car hits the enemy car"""
        #sets the initial crash to false
        crash = False
        #checls whether the Ecar is in the position of the player, if so, it sets crash to true
        if self.y + self.h > 470 and self.y < 470 + self.playerHeight:
            if self.x + self.w > carX and self.x < carX + self.playerWidth: #minus/plus width and height as this is the area (hitbox) of the rectangle
                crash = True
        return crash
    
    
    def resetloop(self):
        '''resets x and y positions of car so that it can loop, this is the same for all cars otherwise they would continue to crash'''
        #resets x and y
        self.y = -100
        self.x = R.randrange(100,(700-self.w))
        
    def resetCars(self):
        ''''resets the x and y positions of car once the game has eneded, this is to the initial pos'''
        #resets x and y
        self.y = self.initialY
        self.x = R.randrange(100,(700-self.w))

def checkScore(score):
    """Checks the score in order to determine how hard to send the cars
    This is done by checking each time the score reaches 5, each multiple of five a new harder car is realeased

    Args:
        score: checks the score in order to determine how hard the game is
    Returns:
        Difficulty: Difficulty whic hdetermines how hard the game is

    Raises:
        none
    """
    #the scores multiple of five
    remainder = score % 5
    score = (score - remainder)/5
    
    #sets difficulty per score 
    if score == 0:
        difficulty = 1
    #difficulty varies on score becasue as more cars are added the score increments faster
    elif score >= 1 and score < 4:
        difficulty = 2
    elif score >= 4 and score < 7:
        difficulty = 3
    elif score >= 7 and score < 12:
        difficulty = 4
    elif score >= 12 and score < 19:
        difficulty = 5
    elif score >= 19:
        difficulty = 6
        
    return difficulty
    
    
    
def load(name):
    """loads media and returns a varaiable
    This module will be used whenever you would like to render media, the benefit of putting this in a function is that it can return a specific error code
    Args:
        name: path where the media is located
    Returns:
        tempV = varaible of the loaded media
    Raises:
        error if file is not found
    """
    #trys to load the media, if not found; terminates window and displays an error message
    try:
        tempV = P.image.load(name)
    except :
        print('error: '+name +' could not be found')
        P.quit()   # stops the game engine
        sys.exit()  # close operating system window
    return tempV

