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
from mods import * #imports modules from mods file
from Highscores import * #imports the class from highscores file

#loads all graphics, this has to be done early as they are used when passing to objects
try:
    road = P.image.load('media/Background Road.png')
    mainBackground = P.image.load('media/Background Main.png')
    highscoreBackground = P.image.load('media/Background Highscore.png')
    crashBackground = P.image.load('media/Background crash.png')
    
    carImage = P.image.load('media/red car.png')
    carImageL = P.image.load('media/red car left.png')
    carImageR = P.image.load('media/red car right.png')
    
    enemy0 = P.image.load('media/enemy 0.png')
    enemy1 = P.image.load('media/enemy 1.png')
    enemy2 = P.image.load('media/enemy 2.png')
    enemy3 = P.image.load('media/enemy 3.png')
    enemy4 = P.image.load('media/enemy 4.png')
    enemy5 = P.image.load('media/enemy 5.png')
    enemy6 = P.image.load('media/enemy 6.png')
    
    lImage = P.image.load('media/left.png')
    lImageH = P.image.load('media/left highlight.png')
    rImage = P.image.load('media/right.png')
    rImageH = P.image.load('media/right highlight.png')
    
    gButton = P.image.load('media/green button.png')
    rButton = P.image.load('media/red button.png')
    sButton = P.image.load('media/stone button.png')
    bButton = P.image.load('media/blue button.png')
    
    gButtonH = P.image.load('media/green button.png')
    rButtonH = P.image.load('media/red button.png')
    sButtonH = P.image.load('media/stone button.png')
    bButtonH = P.image.load('media/blue button.png')
    
    playerWidth = P.Surface.get_width(carImage) #gets the player width
    playerHeight = P.Surface.get_height(carImage) #gets the player height
except:
    print("images could not be found")
    


# pygame setup - only runs once
P.init()  # starts the game engine
clock = P.time.Clock()  # creates clock to limit frames per second
loopRate = 60  # sets max speed of main loop
SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 800, 600  # sets size of screen/window
screen = P.display.set_mode(SCREENSIZE)  # creates window and game screen
P.display.set_caption("Racing to the end of the universe!") #sets the game window caption
play = True #controls the game loop

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
playB = button(screen,gButton,gButtonH,"PLAY",30,black,"play")
highscoreB = button(screen,bButton,bButtonH,"HIGHSCORES",30,black,"highscore")
instructionsB = button(screen,sButton,sButtonH,"INSTRUCTIONS",30,black,"instructions")
introB = button(screen,rButton,rButtonH,"BACK",30,black,"intro")
mainMenuB = button(screen,rButton,rButtonH,"MAIN MENU",30,black,'mainMenu')
saveB = button(screen,sButton,sButtonH,"SAVE",30,black,'save')
todayB = button(screen,sButton,sButtonH,"TODAYS",30,black,'today')
overallB = button(screen,sButton,sButtonH,"OVERALL",30,black,'overall')

#creates objects to be used later on in arrowButton class
leftB = arrowButton(screen,lImage,lImageH,"left")
rightB = arrowButton(screen,rImage,rImageH,"right")

#creates objects to be used later in player class
mcar = player(screen,carImage,carImageL,carImageR) #main player car

#creates the enemy cars to be used later on
Ecar0 = Ecar(screen,enemy0,5,-150,playerWidth,playerHeight)
Ecar1 = Ecar(screen,enemy1,5,-300,playerWidth,playerHeight)
Ecar2 = Ecar(screen,enemy2,5,-450,playerWidth,playerHeight)
Ecar3 = Ecar(screen,enemy3,5,-600,playerWidth,playerHeight)
Ecar4 = Ecar(screen,enemy4,5,-750,playerWidth,playerHeight)
Ecar5 = Ecar(screen,enemy5,5,-900,playerWidth,playerHeight)
Ecar6 = Ecar(screen,enemy6,5,-1050,playerWidth,playerHeight)

#creates two objects of Highscores which will be refered to acess methods ass well as printing scores
HST = highscore(screen,'Todays Highscores')
HS = highscore(screen,'Highscores')


#creating a dictionary that referes to each of the enemy car objects, this is to make it easier to call them later
enemyCarDict = {
    0 : Ecar0,
    1 : Ecar1,
    2 : Ecar2,
    3 : Ecar3,
    4 : Ecar4,
    5 : Ecar5,
    6 : Ecar6,
    }
#creates a dictionary that refers to which playScreen to display (this is referenced later within the class
dispatch = {
        'intro' : 'introscreen',
        'play' : 'playGame',
        'instructions' : 'instructionScreen',
        'crash' : 'crashScreen',
        'highscore' : 'highscoreScreen',
            }



class game():
    """Game loop! contians all of the different screens in different methods....

    Attributes:
            #creates initial variables that will be used
        self.carX = 375 :x cordinate for car
        self.playScreen = "intro" :intialises what screen to start on
        self.score = 0 :initialises score because theres no headstarts here
        self.name = '' :def __init__(self,screen,carImage,carImageL,carImageR):name of the persons highscore
        self.roadY = 0 : Controlls where the road is at as it scrolls
        """
        
    def __init__(self):
        '''creates initial variables that will be used'''
        self.carX = 375 
        self.playScreen = "intro" 
        self.score = 0 
        self.name = ''
        self.saved = False
        self.today = False
        self.roadY = 0
        

        
    def introscreen(self):
        """Displays the intro screen
        Made up of a background, buttons and text

        """
        screen.blit(mainBackground, (0,0)) #blits the image background
        
        self.playScreen = playB.draw(50,500, self.playScreen) 
        self.playScreen =highscoreB.draw(575,500, self.playScreen)
        self.playScreen =instructionsB.draw(325,500, self.playScreen)
        
    def playGame(self):
        """Displays the game screen
        this will then reference to other classes

        """

        #creates the scrolling background image
        scrollY = self.roadY % road.get_rect().height #scrollY is the Y coordinate that the image will be displayed, this is the remiander of roadY when dividied by the image height
        screen.blit(road, (-25,scrollY - road.get_rect().height)) #displays the image to the screen, x is -25 due to the original image size, x has to minus height otherwise there would be unused space
        if scrollY < SCREENHEIGHT: #Creates a looping road with a second image while the first is reset to its original position (blitting an image with normal scrollY)
            screen.blit(road, (-25,scrollY)) 
        self.roadY += 3 #controls the speed at which it scrolls
        
        oldCarX = self.carX #creates a temporary variable which will be checked later on to see if the x postion has been changed
        #draws left and right buttons
        self.carX = leftB.draw(25,500,self.carX)
        self.carX = rightB.draw(700,500,self.carX)
        
        if oldCarX > self.carX: #checks whether the car has been moved left or right
            movement = 'left'
        elif oldCarX < self.carX:
            movement = 'right'
        else:
            movement = None
        
        difficulty = checkScore(self.score) #checks the difficulty in order to determine how many cars to deply
        
        for i in range (0,difficulty): #deploys cars according to how hard the difficutly is
            self.score = enemyCarDict[i].draw(self.score)
            
        
        mcar.draw(self.carX,movement) #draws the main player rectangle car
        



        rTxt(screen,("Score: "+str(self.score)),100,50,48,black)  #draws the score  
        self.playScreen = introB.draw(600,50,self.playScreen) #draws the back button which only will be used to go back to the intro screen
        
        for i in range (0,difficulty): #checks all the cars that are depolyed
                crash = enemyCarDict[i].checkHit(self.carX) #checks if the car hits the enemy car
                if crash == True:
                    self.playScreen = "crash" #sends to crash screen
            
        if self.carX>550 + playerWidth or self.carX<100: #creates a boundry that the car must stay in, uses get width as this depends on the size of the grahpic of the car
            self.playScreen = "crash"

    def instructionScreen(self):
        """Displays the instructions screen
        this will then reference to other classes

        """
        screen.fill(black) #fills the screen with a background colour
        rTxt(screen,"Instructions",400,50,48,white)
        self.playScreen = introB.draw(600,50, self.playScreen) #draws the back button for the intro screen
    
    def highscoreScreen(self):
        """Displays the highscore screen
        this will then reference to other classes
        """
        screen.blit(highscoreBackground, (0,0)) #blits the image background
        self.playScreen = introB.draw(600,50, self.playScreen) #draws the back button for the intro screen

            
        if self.today == True: #checks which highscores to display
            press = todayB.draw(600,500, self.playScreen) #draws buttons to switch between highscore screens
            rTxt(screen,"Overall Highscores",400,50,48,white) #draws the title of the screen
            HS.printHighscore(white) #refers to method to print text
            
        if self.today == False:
            press = overallB.draw(600,500, self.playScreen)
            rTxt(screen,"Todays Highscores",400,50,48,white)
            HST.printHighscore(white)

        if press == True:
            self.today = False
        if press == False:
            self.today = True
        
    def crashScreen(self):
        """Displays the crash screen when a boundry is met
        this will reference to other classes and modules to display a screen
        """
        save = False #states whether the name is saved or not  
        
        crashBackground
        screen.blit(crashBackground, (100,50)) #blits the  crash image background
        
        
        rTxt(screen,"You crashed!",400,100,48,black) #displays text saying you crashed
        rTxt(screen,("Score: "+str(self.score)),400,200,48,black) #displays your score
        self.playScreen = mainMenuB.draw(150,450,self.playScreen) #draws a main menu button
        
        if self.saved == False:
            rTxt(screen,"Name: ",200,275,48,black) #displays text
            P.draw.rect(screen,black,(300,250,300,50),5) #border for name input
            save = saveB.draw(450,450,self.playScreen) #draws the save button
            
            
            for event in P.event.get(): #gets any events from the user
                if event.type == P.QUIT:  # tests if window's X (close) has been clicked
                    P.quit()   # stops the game engine
                elif event.type == P.KEYDOWN: #checks if the event is a key press
                    if event.key == P.K_BACKSPACE: #If the event is a backspace it will take away a character from the string
                        self.name = self.name[0:-1]
                    elif event.key == P.K_TAB or event.key == P.K_RETURN:
                        pass #cant put a tab within the name as this is what seperates variables
                    else:
                        if len(self.name) < 10: #limit of characters is 10
                            self.name += event.unicode #adds the letter or symbol to the name
        
                        

            rTxt(screen,self.name,400,275,48,black) #draws the name
        
        
        if self.playScreen == "intro": #if the palyer wants to go to the main menu, positions must be reset
            self.carX = 375 #car reset positon
            self.score = 0 # resets the score
            self.name = '' #resets the name
            self.saved = False #resets the saved variable
            for i in range (0,6): #becasue difficulty is not passed we will reset all of the cars, this is okay because it is done rarely 
                enemyCarDict[i].resetCars() #calls class method to reset the value of the coordinates for each object
                
        
        
        if save == True:
            self.name = HS.appendFile(self.name,self.score)
            if self.name == '':
                self.saved = False
            else:
                self.saved = True
                print("score was saved")
            
            
    def gameloop(self):
        ''' determines what screen to display based on playscreen'''

        getattr(self, dispatch[self.playScreen])() #gets the key from the dictionary


#this varaible has to be created after the game class has been interprited
game = game()


# game loop - runs loopRate times a second!
while play:  # game loop - note:  everything in this loop is indented one tab
    
    game.gameloop()
    
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



