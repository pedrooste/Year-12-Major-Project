""" Racing to the end of the universe!
A simple car game involving pygame. You control a car on a road in which you have to dodge oncomming cars, this will get harder as the game progresses.
"""

__authorimport__ = "Pedro Oste"
__license__ = "GPL"
__version__ = "1.0.2"
__email__ = "Pedro.oste@education.nsw.com.au"
__status__ = "release"

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
#dependencies
import pygame as P # accesses pygame files
import sys  # to communicate with windows
import random as R #import the random function
from mods import * #imports modules from mods file
from Highscores import * #imports the class from highscores file
import time as T #imports time module

# pygame setup - only runs once
P.init()  # starts the game engine
clock = P.time.Clock()  # creates clock to limit frames per second
loopRate = 60  # sets max speed of main loop
SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 800, 600  # sets size of screen/window
screen = P.display.set_mode(SCREENSIZE)  # creates window and game screen
P.display.set_caption("Racing to the end of the universe!") #sets the game window caption
play = True #controls the game loop

#loads all graphics, this has to be done early as they are used when passing to objects 
road = load('media/Background Road.png')
mainBackground = load('media/Background Main.png')
highscoreBackground = load('media/Background Highscore.png')
squareBackground = load('media/Background crash.png')
instructionsBackground = load('media/Background Instructions.png')

carImage = load('media/red car.png')
carImageL = load('media/red car left.png')
carImageR = load('media/red car right.png')

enemy0 = load('media/enemy 0.png')
enemy1 = load('media/enemy 1.png')
enemy2 = load('media/enemy 2.png')
enemy3 = load('media/enemy 3.png')
enemy4 = load('media/enemy 4.png')
enemy5 = load('media/enemy 5.png')
enemy6 = load('media/enemy 6.png')

lImage = load('media/left.png')
lImageH = load('media/left highlight.png')
rImage = load('media/right.png')
rImageH = load('media/right highlight.png')

gButton = load('media/green button.png')
rButton = load('media/red button.png')
sButton = load('media/stone button.png')
bButton = load('media/blue button.png')

gButtonH = load('media/green button highlight.png')
rButtonH = load('media/red button highlight.png')
sButtonH = load('media/stone button highlight.png')
bButtonH = load('media/blue button highlight.png')

#loads the sfx into a variable with error checking
try:
    backgroundMuisc = P.mixer.music.load('media/background sfx.wav')
    crashMusic = P.mixer.Sound('media/crash sfx.wav')
except:
    print('error loading sfx') #Error statement
    P.quit()   # stops the game engine
    sys.exit()  # close operating system window

# sets global variables for some colours if you want them RGB (0-255)
white = (255, 255, 255)
black = (0, 0, 0)
red = (216, 0, 0)
yellow = (234, 226, 0)
green = (0, 206, 44)
blue = (5, 0, 165)
grey = (92, 98, 112)

#creates objects to be used later on in button class
playB = button(screen,gButton,gButtonH,"PLAY",30,black,"play")
highscoreB = button(screen,bButton,bButtonH,"HIGHSCORES",30,black,"highscore")
instructionsB = button(screen,sButton,sButtonH,"INSTRUCTIONS",30,black,"instructions")
introB = button(screen,rButton,rButtonH,"BACK",30,black,"intro")
pauseB = button(screen,rButton,rButtonH,"PAUSE",30,black,"pause")
mainMenuB = button(screen,rButton,rButtonH,"MAIN MENU",30,black,'mainMenu')
saveB = button(screen,sButton,sButtonH,"SAVE",30,black,'save')
todayB = button(screen,sButton,sButtonH,"TODAYS",30,black,'today')
overallB = button(screen,sButton,sButtonH,"OVERALL",30,black,'overall')

#creates objects to be used later on in the button class, but uses a differnt method
leftB = button(screen,lImage,lImageH,None,None,None,"left")
rightB = button(screen,rImage,rImageH,None,None,None,"right")

#creates objects to be used later in player class
mcar = player(screen,carImage,carImageL,carImageR)

#creates varaibles which are used to create the enemy car objectss
playerWidth = P.Surface.get_width(carImage)
playerHeight = P.Surface.get_height(carImage)

#creates the enemy car objects to be used later on
Ecar0 = Ecar(screen,enemy0,5,-150,playerWidth,playerHeight)
Ecar1 = Ecar(screen,enemy1,5,-300,playerWidth,playerHeight)
Ecar2 = Ecar(screen,enemy2,5,-450,playerWidth,playerHeight)
Ecar3 = Ecar(screen,enemy3,5,-600,playerWidth,playerHeight)
Ecar4 = Ecar(screen,enemy4,5,-750,playerWidth,playerHeight)
Ecar5 = Ecar(screen,enemy5,5,-900,playerWidth,playerHeight)
Ecar6 = Ecar(screen,enemy6,5,-1050,playerWidth,playerHeight)

#creates two objects of Highscores which will be refered to when using the highscore class
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
#creates a dictionary that refers to which playScreen to display (this is referenced later within the play class)
dispatch = {
        'intro' : 'introscreen',
        'play' : 'playGame',
        'instructions' : 'instructionScreen',
        'crash' : 'crashScreen',
        'highscore' : 'highscoreScreen',
        'pause' : 'pauseScreen',
        }



class game():
    """Game loop! contains all of the different screens in different methods....

    Attributes:
        self.carX: x cordinate for car
        self.playScreen: intialises what screen to start on
        self.score : initialises score because theres no headstarts here
        self.name: name of the persons highscore
        self.saved: Controlls whether the highscore was saved or not
        self.today: Controlls whether todays date is the same as the todays highscore file
        self.roadY: Controlls where the road is at as it scrolls
        self.countdown: Controlls the number that the game will countdown from
        self.playerWidth: Gets the width of the player to later check for collisions
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
        self.countdown = 3
        self.playerWidth = P.Surface.get_width(carImage)

        
    def introscreen(self):
        """Displays the intro screen
        Made up of a background, buttons and text

        """
        #displaying the background
        screen.blit(mainBackground, (0,0))
        #displaying the buttons, also checking if they are pressed
        self.playScreen = playB.drawNav(50,500, self.playScreen) 
        self.playScreen =highscoreB.drawNav(575,500, self.playScreen)
        self.playScreen =instructionsB.drawNav(325,500, self.playScreen)
        
    def playGame(self):
        """Displays the game screen
        this will then reference to other classes

        """
            
        #creates the scrolling background image
        scrollY = self.roadY % road.get_rect().height #scrollY is the Y coordinate that the image will be displayed
        screen.blit(road, (-25,scrollY - road.get_rect().height)) #displays the image to the screen, have to minus the road height or the image would be displayed above
        if scrollY < SCREENHEIGHT: #Creates a looping road with a second image while the first is reset to its original position (blitting an image with normal scrollY)
            screen.blit(road, (-25,scrollY)) 
        self.roadY += 3 #controls the speed at which it scrolls
        
        oldCarX = self.carX #creates a temporary variable which will be checked later on to see if the x postion has been changed
        
        #draws arrow buttons
        self.carX = leftB.drawArrow(25,500,self.carX)
        self.carX = rightB.drawArrow(700,500,self.carX)
        
        #checking whether the car has moved left or right
        if oldCarX > self.carX:
            movement = 'left'
        elif oldCarX < self.carX:
            movement = 'right'
        else:
            movement = None
        
        #checks the difficulty in order to determine how many cars to deploy
        difficulty = checkScore(self.score)
        #deploys cars according to how hard the difficutly is
        for i in range (0,difficulty):
            self.score = enemyCarDict[i].draw(self.score)
        
        #draws the main player rectangle car 
        mcar.draw(self.carX,movement) 
        
        #draws the score and pause button
        rTxt(screen,("Score: "+str(self.score)),100,50,48,black)
        self.playScreen = pauseB.drawNav(600,50,self.playScreen)
        
        #checks all the cars that are depolyed or collisions
        for i in range (0,difficulty):
                crash = enemyCarDict[i].checkHit(self.carX) #checks if the player car hits the enemy car
                if crash == True:
                    #stops the music, plays crash music and displays crashscreen
                    P.mixer.music.stop()
                    P.mixer.Sound.play(crashMusic)
                    self.playScreen = "crash"
                    
        #creates and checks the boundry the car must stay within (road distance)    
        if self.carX>550 + self.playerWidth or self.carX<100: #this depends on the width of the player car graphic
            #stops the music, plays crash music and displays crashscreen
            P.mixer.music.stop()
            P.mixer.Sound.play(crashMusic)
            self.playScreen = "crash"
            
        #to set a variable only if needed    
        if self.countdown > 0:
            x =325 #x cord to be display text
            P.mixer.music.play()
            
            #Creates a coutndown from self.coutndown
            while self.countdown > 0:
                rTxt(screen,str(self.countdown),x,200,150,white) #displays countdown number
                self.countdown -= 1
                x += 75 #moves x pos so numbers don't display on top of each other
                P.display.flip()  # makes any changes visible on the screen
                T.sleep(1) #sleeps for one second
        
        #stops the music if the game is paused
        if self.playScreen == "pause":
            P.mixer.music.stop()

    def instructionScreen(self):
        """Displays the instructions screen
        this will then reference to other classes

        """
        #displays the background,title and buttons
        screen.blit(instructionsBackground,(0,0))
        rTxt(screen,"Instructions",400,50,48,white)
        self.playScreen = introB.drawNav(600,50, self.playScreen)
    
    def highscoreScreen(self):
        """Displays the highscore screen
        this will then reference to other classes
        """
        #displays the background and back button
        screen.blit(highscoreBackground, (0,0))
        self.playScreen = introB.drawNav(600,50, self.playScreen)

        #checks which highscores to display
        if self.today == False:
            #draws button to switch between highscores, title of the screen and prints overall highscores
            press = todayB.drawNav(600,500, self.playScreen)
            rTxt(screen,"Overall Highscores",400,50,48,white)
            HS.printHighscore(white)
        
        #checks which highscores to display
        if self.today == True:
            #draws button to switch between highscores, title of the screen and prints overall highscores
            press = overallB.drawNav(600,500, self.playScreen)
            rTxt(screen,"Todays Highscores",400,50,48,white)
            HST.printHighscore(white)
        
        #checks if overall button and todays button have been pressed
        if press == True:
            self.today = False
        if press == False:
            self.today = True
        
    def crashScreen(self):
        """Displays the crash screen when a boundry is met
        this will reference to other classes and modules to display a screen
        """
        #states whether to save the score or not
        save = False
        
        #displays the background, crash text, score text and main menu button
        screen.blit(squareBackground, (100,50))
        rTxt(screen,"You crashed!",400,100,48,black)
        rTxt(screen,("Score: "+str(self.score)),400,200,48,black)
        self.playScreen = mainMenuB.drawNav(150,450,self.playScreen)
        
        #checks whether the score has been saved
        if self.saved == False:
            #displays the name text, border for name and save button
            rTxt(screen,"Name: ",200,275,48,black)
            P.draw.rect(screen,black,(300,250,300,50),5)
            save = saveB.drawNav(450,450,self.playScreen)
            
            #gets any events from the user when writing the saved name
            for event in P.event.get():
                if event.type == P.QUIT:  # tests if window's X (close) has been clicked
                    P.quit()   # stops the game engine
                elif event.type == P.KEYDOWN: #checks if the event is a key press
                    if event.key == P.K_BACKSPACE: #If the event is a backspace it will take away a character from the string
                        self.name = self.name[0:-1]
                    elif event.key == P.K_TAB or event.key == P.K_RETURN: #cant put a tab within the name as this is what seperates variables
                        pass
                    else:
                        if len(self.name) < 10: #limit of characters is 10
                            self.name += event.unicode #adds the letter or symbol to the name
            #displays the name
            rTxt(screen,self.name,400,275,48,black)
        
        #varaibles have to be reset if player wants to go to the main menu
        if self.playScreen == "intro":
            game.reset()
                
        #saves file if the save button once if has been pressed
        if save == True:
            self.name = HS.appendFile(self.name,self.score)
            #if the name is blank the score wont save (inappropriate names wont save)
            if self.name == '':
                self.saved = False
            else:
                self.saved = True
            
            
    def pauseScreen(self):
        """Displays the pasue screen when requested
        this will reference to other classes and modules to display a screen
        """
        
        #displays the background, paused and score text and buttons
        screen.blit(squareBackground, (100,50))
        rTxt(screen,"Paused",400,100,48,black)
        rTxt(screen,("Score: "+str(self.score)),400,200,48,black)
        self.playScreen = mainMenuB.drawNav(150,450,self.playScreen)
        self.playScreen = playB.drawNav(450,450,self.playScreen)
        
        #resets the countdown when continued
        if self.playScreen == "play":
            self.countdown = 3
        
        #resets the varaibles if player goes to main menu
        if self.playScreen == "intro":
            game.reset()
            
            
    def reset(self):
        ''' resets all of the varaibles back to their originals'''
        self.carX = 375 #car reset positon
        self.score = 0 #resets the score
        self.name = '' #resets the name
        self.countdown = 3 #resets the countdown
        self.saved = False #resets the saved variable
        for i in range (0,6): #becasue difficulty is not passed we will reset all of the cars, this is okay because it is not done regulary
            enemyCarDict[i].resetCars() #calls class method to reset the value of the coordinates for each object
        
        

        


    def gameloop(self):
        ''' determines what screen to display based on playscreen'''
        #gets the key from the dictionary and find a value to display
        getattr(self, dispatch[self.playScreen])()
    #END OF GAME CLASS



#this varaible has to be created after the game class has been interprited
game = game()

# game loop - runs loopRate times a second!
while play:  # game loop - note:  everything in this loop is indented one tab
    
    #runs the gameloop class
    game.gameloop()
    for event in P.event.get():  # get user interaction events
        if event.type == P.QUIT:  # tests if window's X (close) has been clicked
            play = False  # causes exit of game loop
    
    # code ends
    P.display.flip()  # makes any changes visible on the screen
    clock.tick(loopRate)  # limits game to frame per second, FPS value

# out of game loop #
print("Thanks for playing mate")  # notifies user the game has ended
P.quit()   # stops the game engine
sys.exit()  # close operating system window



