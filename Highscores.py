""" Racing to the end of the universe!
A simple car game involving pygame. You control a car on a road in which you have to dodge oncomming cars, this will get harder as the game progresses.

this is where the classes for highscores will be stored!
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



import pygame as P # accesses pygame files
import sys  # to communicate with windows
import datetime as d
import os #to communicate with the OS
from mods import * #imports modules from mods file

class highscore():
    """Deals with the lists and files relating to highscore

    This is not so much for storing objects but creating ease of passing varaibles between methods, the objects are only created for printing out highscores

    Attributes:
        self.fileName: file to refer to 
        self.list: creates a list of the file when calling organise file
        self.HST: directory of todays highscores file
        self.HS: directory of overall highscore file
        self.screen: pygame screen to display to
    """

    def __init__(self,screen,fileName):
        """Inits SampleClass with variables."""
        self.fileName = fileName
        self.list = None
        self.HST = 'Todays Highscores'
        self.HS = 'Highscores'
        self.screen = screen

    def organiseFile(self):
        """Organises the file and creates a list, this is called when printing the highscores as they need to be sorted."""
        #creates a temp empty list
        highscoreList = []
        
        #trys to find the file and load it into a list
        try:
            with open('media/'+self.fileName+'.txt', 'r') as file:
                for line in file.readlines(): 
                    list = line.split('\t') #spilts the original file into a list of three
                    list1 = list[0] #creates an individual of each to create a final list later
                    list2 = int(list[1]) #has to make an int otherwise it will sort it as if its an str 
                    list3 = list[2]
                    list3 = (list3[0:((len(list[2]))-1)])
                    list = [list1,list2,list3]
                    highscoreList.append(list) #creates a temp list of highscores
                        
            highscoreList.sort(key= lambda x: x[1], reverse = True) #sorts the list, reverse order as it naturally sorts low to high

            self.list = highscoreList #this then creates the final list
        #if it cant find the file...
        except:
            print('there is no file specified') #debugging statement
            self.list = [] #returns an empty list

    def checkdate(self):
        ''' checks the date to determine whether the file contains highscore from the current day '''
        #trys to open the file in order to check the date
        try:    
            with open('media/'+self.HST+'.txt', 'r') as file:
                list = file.readline() #reads the first file line (as all scores have the same date)
                list = list.split('\t') #spilts the original file line into a list of three
                dateCheck = list[2] #gets the date to check ,do not need to check them all as they all are the same
                dateCheck = dateCheck[0:((len(list[2]))-1)]
                if str(d.date.today()) == dateCheck:
                    #creates an easy to use boolean
                    today = True
                else:
                    today = False
        except:
            today = True
        return today #returns for further use
    
    def appendFile(self,name,score):
        '''Appends data to both of the highscore files, as well as checking if the today highscores are the correct date'''
        
        #checking if the name is inappropriate
        inappropriate = self.checkName(name)
        while inappropriate == True:
            print('Inappropriate name')
            name = ''
            return name #returns an empty name
        
        #creates todays date    
        date = str(d.date.today())
        
        #appends the score to the overall highscores file
        with open('media/'+self.HS+'.txt','a') as file: #Will create a new file if there is not one there, use append to not overwrite data
            file.write(name+'\t'+str(score)+'\t'+ date +'\n') #writes to the file
        
        #checks the date in order to determine if the file needs to be cleared (old date)
        today = self.checkdate()
        
        #if the date is not current, the programme will remove the file and create a new one
        if today == False:
            print('old dated score, removing file ') #debugging statement
            os.remove('media/'+self.HST+'.txt') #removes the file if the dates are not current (whipes all highscores)
            with open('media/'+self.HST+'.txt','a') as file: #Will create a new file if there is not one there, use append to not overwrite data
                file.write(name+'\t'+str(score)+'\t'+ date +'\n') #writes to the file
                
        #otherwise the score is normally appended
        else:
            with open('media/'+self.HST+'.txt','a') as file: #Will create a new file if there is not one there, use append to not overwrite data
                file.write(name+'\t'+str(score)+'\t'+ date +'\n') #writes to the file
        return name
    
    def printHighscore(self,colour):
        '''method to print out the highscore'''
        
        #calls to organise file before printing
        self.organiseFile()
        #trys to print top 5 scores
        try:
            #sets temp var
            y = 200
            for line in range(0,5):
                #displays all highscores down a row
                rTxt(self.screen,(str(line+1)+'. '+self.list[line][0]+': '+str(self.list[line][1])),400,y,48,colour)
                y += 50
        
        #if there are not five scores
        except:
            y = 200
            for line in range(0,(len(self.list))):
                #displays all highscores down a row
                rTxt(self.screen,(str(line+1)+'. '+self.list[line][0]+': '+str(self.list[line][1])),400,y,48,colour)
                y += 50
    
    def checkName(self,name):
        '''Checks if the name that is input is appropriate or not'''
        #initiates inappropriate as false
        inappropriate = False
        name = name.lower()
        print(name)
        #trys to open and read name check file
        try:   
            with open('media/Name check.txt', 'r') as file:
                list = file.read() #reads the file
            list = list.split('\t') #spilts the original file line into a list of three
            name.strip() #strips the name of any symbols
            for word in list: #checks each word in list
                if word == name: 
                    inappropriate = True
                    break
        #if file could not be found...            
        except:
            print("Name check file could not be found")
        
        return inappropriate #returns a boolean whether its appropriate or not




