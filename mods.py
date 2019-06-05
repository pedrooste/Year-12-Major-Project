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


"""

#import statements for any dependencies
import pygame as P
import random as R
import time as T

class button():
    """Creates a button with text

    Each object will be created with a number of vairables, these are then rendered out if the draw method is called.
    draw method will draw a lighter rectangle if the mouse is in the same position, also checking if clicked.

    Attributes:
        self.colour = colour of the rectangle
        self.hColour = colour of the rectangle when mouse is over it
        self.w = width of rectangle
        self.h = height of rectangle
        self.txt = text to be displayed inside of rectangle
        self.size = size of text
        self.tColour = colour of text
        self.action = determines what the buttons action is when clicked
    """
    def __init__ (self,colour,hColour,w,h,txt,size,tColour,action):
        self.colour = colour
        self.hColour = hColour
        self.w = w
        self.h = h
        self.txt = txt
        self.size = size
        self.tColour = tColour
        self.action = action

    def draw(self,screen,x,y,playScreen):
        """method that draws a rectangle on the screen, also checking if the mouse is over the rectangle, if it is it will also check for a click."""
        mouse= P.mouse.get_pos() #gets X and Y of mouse position
        
    
        if x+self.w>mouse[0]>x and y+self.h>mouse[1]>y: #asks if the mouse is in the region where the button is located.
            P.draw.rect(screen,self.hColour,(x,y,self.w,self.h)) #draws a rectangle with the highlighted colour if mouse is on it
            
            for event in P.event.get():
                P.event.get() #gets postion of mouse when clicked
                if event.type == P.MOUSEBUTTONUP and self.action!=None: #asks if the button has been clicked when it is within the reigion and if action is doing nothing
                    if self.action=="play": #determines which action to fufil
                        playScreen = "play"
                    elif self.action =="instructions":
                        playScreen = "instructions"
                    elif self.action =="intro":
                        playScreen = "intro"
                    elif self.action =="mainMenu":
                        playScreen = "intro"
                    elif self.action =="highscore":
                        playScreen = "highscore"
                    elif self.action == "save":
                        save = True
                        return save #returns save instead of playScreen
                    elif self.action == "today":
                        press = True
                        return press #returns whether this button was pressed or not
                    elif self.action == "overall":
                        press = False
                        return press
                    
        else:
            P.draw.rect(screen,self.colour,(x,y,self.w,self.h)) #draws a rectangle with the normal colour if mouse isnt on it
        font = P.font.SysFont('comicsans', self.size) #now we draw the text onto the button (first we have to render)
        text = font.render(self.txt, 1,self.tColour)
        screen.blit(text, (x + (self.w/2 - text.get_width()/2), y + (self.h/2 - text.get_height()/2)))
        return playScreen
    

class arrowButton():
    """This class will be used to draw buttons and check if they have been clicked.

    This is very similar to the class button however is different as a image will be blit rather than a rectangle in the future

    Attributes:
        self.colour = colour of the rectangle
        self.hColour = colour of the rectangle when mouse is over it
        self.w = width of rectangle
        self.h = height of rectangle
        self.action = determines what the buttons action is when clicked
    """

    def __init__(self,colour,hColour,w,h,action):
        """Inits arrowButton with varaibles."""
        self.colour = colour
        self.hColour = hColour
        self.w = w
        self.h = h
        self.action = action

    def draw(self,screen,x,y,carX):
        """method that draws a rectangle on the screen, also checking if the mouse is over the rectangle, if it is it will also check for a click.
        - If the button is clicked, the carX variable will be updated (left and right)
"""
        mouse= P.mouse.get_pos() #gets X and Y of mouse position
        click= P.mouse.get_pressed() #gets postion of mouse when clicked
        
        if x+self.w>mouse[0]>x and y+self.h>mouse[1]>y: #asks if the mouse is in the region where the button is located.
            P.draw.rect(screen,self.hColour,(x,y,self.w,self.h)) #draws a rectangle with the highlighted colour if mouse is on it
            if click[0]==1 and self.action!=None: #asks if the button has been clicked when it is within the reigion and if action is doing nothing
                if self.action =="right": #determines which action to fufil
                    carX +=5 #car x position is updated
                elif self.action =="left":
                    carX -=5

        else:
            P.draw.rect(screen,self.colour,(x,y,self.w,self.h)) #draws a rectangle with the normal colour if mouse isnt on it
           
        return carX

class player():
    """Creates a rectangle that is controlled by the player (x movements) via previous buttons

    This class will be updated accordingly as more graphics are implemented into the game
    
    Attributes:
        self.colour = colour of the rectangle
        self.hColour = colour of the rectangle when mouse is over it
        self.w = width of rectangle
        self.h = height of rectangle
    """

    def __init__(self,colour,hColour,w,h):
        """Inits Player class with variables"""
        self.colour = colour
        self.hColour = hColour
        self.w = w
        self.h = h

    def draw(self,screen,x,movement):
        """method that draws the player onto the screen"""
        if movement == True:
            P.draw.rect(screen,self.hColour,(x,490,self.w,self.h)) #draws a rectangle with the highlighted colour if it has been moved
        else:
            P.draw.rect(screen,self.colour,(x,490,self.w,self.h)) #draws a rectangle with the normal colour if not moved

def rTxt(screen,msg,x,y,size,colour):
    """Renders and blits text
    This module will be used whenever you would like to render text into the pygame window .This is not a class as text wouldnt be treated as an object.
    Args:
        msg: text to be displayed
        x: x value the button will be placed
        y: y value the button will be placed
        l: length of the button
        h: height of the button
        size: size of text
        colour: colour of text
    Returns:
        description of the stuff that is returned by the function.
    Raises:

    """
    
    font = P.font.SysFont("comic sans",size) #creates a font for the render function to use
    text = font.render(msg,True,colour) #creates a text for the blit function to use
    x,y = ((x- (text.get_rect().w/2)),(y- (text.get_rect().h/2))) #centres the text depening on the length and height of the text
    screen.blit(text,(x,y))

class Ecar():
    """creates objects for the variety of enemy cars

    each enemy car will have diffrent speeds and lenghts (to be implemented) ....

    Attributes:
        self.colour = colour of the rectangle
        self.hColour = colour of the rectangle when mouse is over it
        self.w = width of rectangle
        self.h = height of rectangle'
        self.y = starting y postion of the car (this is started at -10 so that it does not instantly appear on start of the game)
        self.x = x postion of the car which will be random between the road boundry
    """

    def __init__(self,colour,speed,y,w,h):
        """Inits SampleClass with blah."""
        self.colour = colour
        self.speed = speed
        self.w = w
        self.h = h
        self.y = y
        self.initialY = y
        self.x = R.randrange(100,(700-w)) #minus width as the area of the car could exceed the boundry

    def draw(self,screen,score):
        """Draws the moving enemy car object"""
        P.draw.rect(screen,self.colour,(self.x,self.y,self.w,self.h)) #draws a rectangle with a colour
        if self.y > 800: #checks if the object is passed, to which it will reset to be shown again
            self.resetloop()
            score = score + 1 #increments score each time a car is passed (or in this case reset)
            print("The score is " + str(score)) #debugging statement
        else:
            self.y = self.y + self.speed #creates a moving image as the loop is fulfilled

        return score
        
    def checkHit(self,carX):
        """checks if the player car hits the enemy car"""
        crash = False #sets crash to false
        if self.y + self.h > 490 and self.y < 490 +50: #sets crash to true if in the players car area
            if self.x + self.w > carX and self.x < carX +50: #minus/plus width and height as this is the area (hitbox) of the rectangle
                crash = True
        return crash
    
    
    def resetloop(self): #reset function to be called, resest x and y.
        self.y = -100 #resets back to an original position
        self.x = R.randrange(100,(700-self.w))
        
    def resetCars(self):
        self.y = self.initialY
        self.x = R.randrange(100,(700-self.w))

def checkScore(score):
    """Checks the score in order to determine how hard to place the cars

    This is done by checking each time the score reaches 5, each multiple of five a new harder car is realeased

    Args:
        score: checks the score in order to determine how hard the game is


    Returns:
        Difficulty: Difficulty whic hdetermines how hard the game is

    Raises:

    """
    remainder = score % 5 #finds the remainder
    score = (score - remainder)/5 #minus the score to a multiple of 5, then divides to find difficulty
    if score == 0: #sets difficulty per score
        difficulty = 1
    elif score >= 1 and score < 4: #difficulty varies on score becasue as more cars are added the score increments faster
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
    


# templates
def function_name(arg1, arg2, other_silly_variable=None):
    """Does something amazing.

    a much longer description of the really amazing stuff this function does and how it does it.

    Args:
        arg1: the first argument required by the function.
        arg2: the second argument required by the function.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        description of the stuff that is returned by the function.

    Raises:
        AnError: An error occurred running this function.
    """
    pass



class SampleClass(object):
    """Summary of class here.

    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam=False):
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""



