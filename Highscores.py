import pygame as P # accesses pygame files
import sys  # to communicate with windows
import datetime as d
import os







class highscore():
    """Deals with the lists and files relating to highscore

    This is not so much for storing objects but creating ease of passing varaibles between methods, the objects are only created for printing out highscores

    Attributes:
        self.fileName = fileName : file to refer to 
        self.list = None : creates a list of the file
            self.HST = 'Todays Highscores' : directory of todays highscores file
        self.HS = 'Highscores' : directory of overall highscore file
    """

    def __init__(self,fileName):
        """Inits SampleClass with variables."""
        self.fileName = fileName
        self.list = None #this remains empty for now
        self.HST = 'Todays Highscores'
        self.HS = 'Highscores'

    def organiseFile(self):
        """Organises the file and creates a list, this is called when printing the highscores as they need to be sorted."""
        highscoreList = [] #creates empty list
        try: #trys to find the file
            with open('media/'+self.fileName+'.txt', 'r') as file:
                for line in file.readlines(): 
                    list = line.split('\t') #spilts the original file into a list of three
                    list1 = list[0] #creates an individual of each to create a final list later
                    list2 = int(list[1]) #has to make an int otherwise it will sort it as if its an str 
                    list3 = list[2]
                    list3 = (list3[0:((len(list[2]))-1)])
                    list = [list1,list2,list3]
                    highscoreList.append(list) #creates a list of highscores
                    
            highscoreList.sort(key= lambda x: x[1], reverse = True) #sorts the list, reverse order as it naturally sorts low to high

            self.list = highscoreList #this then creates a list
        
        except:
            print('there is no file specified') #debugging statement

    def checkdate(self):
        ''' checks the date to determine whether the file contains highscore from the current day '''
        try:
            
            with open('media/'+self.HST+'.txt', 'r') as file: #trys to open the file
                list = file.read() #reads the file
                list = list.split('\t') #spilts the original file line into a list of three
                dateCheck = list[3] #gets the date to check ,do not need to check them all as they all are the same
                dateCheck = dateCheck[0:((len(list[2]))-1)]
                    
                if d.date.today == dateCheck:
                    today = True #creates an easy to use boolean
                else:
                    today = False
        except:
            today = True
        
        return today #returns to further use
    
    def appendFile(self):
        '''Appends data to both of the highscore files, as well as checking if the today highscores are the correct date'''
        
        name  = input('What is your name') #temp test
        inappropriate = self.checkName(name)
        while inappropriate == True:
            print('Inappropriate name')
            name = input('What is your name') #temp test
            inappropriate = self.checkName(name)
            
        score = input('what is your score') #temp test
        date = str(d.date.today()) #creates todays date

        with open('media/'+self.HS+'.txt','a') as file: #Will create a new file if there is not one there, use append to not overwrite data
            file.write(name+'\t'+score+'\t'+ date +'\n') #writes to the file
        today = self.checkdate()
        
        if today == False: 
            os.remove('media/'+self.HST+'.txt') #removes the file if the dates are not current (whipes all highscores)
            with open('media/'+self.HST+'.txt','a') as file: #Will create a new file if there is not one there, use append to not overwrite data
                file.write(name+'\t'+score+'\t'+ date +'\n') #writes to the file
        else:
            with open('media/'+self.HST+'.txt','a') as file: #Will create a new file if there is not one there, use append to not overwrite data
                file.write(name+'\t'+score+'\t'+ date +'\n') #writes to the file            
    
    def printHighscore(self): #prints the highscores
        '''Temporary method to print out the highscore'''
        self.organiseFile() #calls to organise file before printing
        try:
            print('congratulations',self.list[0][0],'you scored',self.list[0][1]) #prints highest score
        except:
            print('there is no data to print highscores') #if organiseFile cant find the file, then there is nothing to print here (debugging statement)
    
    def checkName(self,name): #checks whether the name is appropriate
        '''Checks if the name that is input is appropriate or not'''
        inappropriate = False #initiates inappropriate as false
        try:   
            with open('media/Name check.txt', 'r') as file:
                list = file.read() #reads the file
            list = list.split('\t') #spilts the original file line into a list of three
            name.strip() #strips the name of any symbols
            for word in list: #checks each word in list
                if word == name: 
                    inappropriate = True
                    break
                    
        except:
            print("Name check file could not be found")
        
        return inappropriate #returns a boolean whether its appropriate or not


#creates the objects for the highscore class
todayHS = highscore('Todays Highscores')
HS = highscore('Highscores')
#HS.appendFile()
HS.appendFile()
HS.printHighscore()



todayHS.printHighscore()
