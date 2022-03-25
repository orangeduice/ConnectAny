# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:07:58 2020

@author: Oscar Jackson
"""

import random
import numpy as np
import matplotlib.pyplot as plt

class GB:
    def __init__(self,h,w):
        self.board = np.zeros((h,w)) #creates numpy 2d array size h by w full of 0.
        #Win number e.g. 4 in a row
        self.winNum = 0
        #These hold Surrounding locations
        #defined by compass
        self.NS = [] 
        self.WE = []
        self.NWSE = []
        self.NESW = []
        #empty Surrounding locations
        self.NS_emp = []
        self.WE_emp = []
        self.NWSE_emp = []
        self.NESW_emp = []
        #They are the periously placed tokens of player1 and 2
        self.PP_P1 = (0,0)
        self.PP_P2 = (0,0)
        #These hold all points to be plotted
        self.x1 = []
        self.y1 = []
        self.x2 = []
        self.y2 = []
        self.x0 = []
        self.y0 = []
        #Win condition var
        self.win = False
        #ai mode
        
        #These are the counts for x in a row for all compass directions for player 1 and 2
        self.NS_win1 = 0
        self.WE_win1 = 0
        self.NWSE_win1 = 0
        self.NESW_win1 = 0
        self.NS_win2 = 0
        self.WE_win2 = 0
        self.NWSE_win2 = 0
        self.NESW_win2 = 0
        #possible ai modes
        self.AImodes = "NS" , "WE" , "NWSE" , "NESW"
        #ai mode of above ^ starts at -1 to select random
        self.AImode = -1
        
    def __str__(self):
        #This function prints the gameboard in the command promp
        #it is flipped to display it correctly
        return str(np.transpose(self.board))
    
    def display(self):
        #This function plots the main display using matplotlib
        #Here the code finds all the empty cells
        self.x0 = []
        self.y0 = []
        for i in range(0,len(self.board[0])):
            for o in range(0,len(self.board)):
                if self.board[o][i] == 0.:
                    self.x0.append(o+1)
                    self.y0.append(i+1)
        #making the plot with matplotlib       
        fig = plt.figure()
        #Background to blue
        fig.set_facecolor('b')
        #sets token colors and size that is proportional to the quauity of them (scales up or down)
        plt.scatter(self.x0,self.y0,c = "white", s = 4000*(1/(len(self.board))))
        plt.scatter(self.x1,self.y1,c = "yellow", s = 4000*(1/(len(self.board))))
        plt.scatter(self.x2,self.y2, c = "red", s = 4000*(1/(len(self.board))))
        #turn axis off
        plt.axis('off')
        #invert y axis to display correctly
        plt.gca().invert_yaxis()
        #Background to blue
        plt.gca().set_facecolor('b')
        #show plot
        plt.show()
        
        
    
        
    def place(self,x,token):
        #Places a given token in the board at x position
        error = False
        #error handling
        try:
            b = self.board[x]
            #counts number of spaces
            temp = np.count_nonzero(b == 0.)
            if temp == 0:
                print("NO you cannot place there, the column it is full")
                error = True
                return error
            #uses logic to place in board if there is space  
            self.board[x][temp-1] = token
            #for player 1
            if token == 1.:
                self.PP_P1 = (x,temp-1)
                self.x1.append(x+1)
                self.y1.append(temp)
            elif token == 2.:
                #for player 2
                self.PP_P2 = (x,temp-1)
                self.x2.append(x+1)
                self.y2.append(temp)
                
            y = temp -1
            #Append all Surrounding locations
            self.NS.append((x,y+1))
            self.NS.append((x,y-1))
            self.WE.append((x+1,y))
            self.WE.append((x-1,y))
            self.NWSE.append((x+1,y+1))
            self.NWSE.append((x-1,y-1))
            self.NESW.append((x+1,y-1))      
            self.NESW.append((x-1,y+1))
            #returns exact location of token placed
            return x,(temp-1)
            
        except:
            print("NO you cannot place there, the column does not exist")
            return "error"
            
        
    def check(self,location,token):
        #this code checks the Surrounding locations for places containing a set token
        #it was however not usd
        w = len(self.board)
        h = len(self.board[0])
        x , y = location
            
        temp1 = []
        temp2 = []
        temp3 = []
        temp4 = []

        for i in range(0,len(self.NS)):    
            if not (self.NS[i][0] == -1 or self.NS[i][1] ==-1 or self.NS[i][0] == w or self.NS[i][1] == h ):
                if self.board[self.NS[i][0]][self.NS[i][1]] == token:
                    temp1.append(self.NS[i])
        
        for i in range(0,len(self.WE)):
            if not ( self.WE[i][0] == -1 or self.WE[i][1] ==-1 or self.WE[i][0] == w  or self.WE[i][1] == h ) :
                if self.board[self.WE[i][0]][self.WE[i][1]] == token:
                    temp2.append(self.WE[i])
        
        for i in range(0,len(self.NESW)):    
            if not (self.NESW[i][0] == -1 or self.NESW[i][1] ==-1 or self.NESW[i][0] == w or self.NESW[i][1] == h ):
                if self.board[self.NESW[i][0]][self.NESW[i][1]] == token:
                    temp3.append(self.NESW[i])
        
        for i in range(0,len(self.NWSE)):
            if not ( self.NWSE[i][0] == -1 or self.NWSE[i][1] ==-1 or self.NWSE[i][0] == w  or self.NWSE[i][1] == h ) :
                if self.board[self.NWSE[i][0]][self.NWSE[i][1]] == token:
                    temp4.append(self.NWSE[i])

        return temp1 , temp2 , temp3, temp4
    
    
    
    def check_win(self):  
        #This function checks for the winning move (RAN OUT OF TIME ONLY 4 IN ROW)
        if (self.NS_win1 == 4):
            print("player wins!")
            return True
        elif (self.WE_win1 == 4):
            print("player wins!")
            return True
        elif (self.NWSE_win1 == 4):
            print("player wins!")
            return True
        elif (self.NESW_win1 == 4)  :
            print("player wins!")
            return True
        elif (self.NS_win2 == 4):
            print("computer wins!")
            return True
        elif (self.WE_win2 == 4):
            print("computer wins!")
            return True
        elif (self.NWSE_win2 == 4):
            print("computer wins!")
            return True
        elif (self.NESW_win2 == 4)  :
            print("computer wins")
            return True
        else:
            return False
    
            
    #The following Functions all count the number of adjacent tokens that are the same in every deriection
    def check_NS(self,location,token):
        self.NS_win1 = 0
        self.NS_win2 = 0
        x , y = location
        while self.board[x][y] == token:
            y = y -1
            if y== -1:
                break
        y = y + 1     
        while self.board[x][y] == token:
            y = y + 1
            if token == 1.:   
                self.NS_win1 = self.NS_win1 + 1
            else:
                self.NS_win2 = self.NS_win2 + 1
            if y == len(self.board[0]):
                break
            
    def check_WE(self,location,token):
        self.WE_win1 = 0
        self.WE_win2 = 0
        x , y = location
        while self.board[x][y] == token:
            x = x -1
            if x == -1:
                break
        x = x + 1
        
        while self.board[x][y] == token:
            x = x + 1
            if token == 1.:   
                self.WE_win1 = self.WE_win1 + 1
            else:
                self.WE_win2 = self.WE_win2 + 1
            if x == len(self.board[0]):
                break
           
    def check_NWSE(self,location,token):
        self.NWSE_win1 = 0
        self.NWSE_win2 = 0
        x , y = location
        while self.board[x][y] == token:
            x = x - 1
            y = y - 1
            if x == -1 or y == -1 :
                break
        x = x + 1
        y = y + 1
        
        while self.board[x][y] == token:
            x = x + 1
            y = y + 1
            if token == 1.:   
                self.NWSE_win1 = self.NWSE_win1 + 1
            else:
                self.NWSE_win2 = self.NWSE_win2 + 1
            if x == len(self.board) or y == len(self.board[0]):
                break
        
    def check_NESW(self,location,token):
        self.NESW_win1 = 0
        self.NESW_win2 = 0
        x , y = location
        while self.board[x][y] == token:
            x = x - 1
            y = y + 1
            #print(x,y)
            if x == -1 or y == len(self.board[0]) :
                break
        x = x + 1
        y = y - 1
        while self.board[x][y] == token:
            x = x + 1
            y = y - 1
            if token == 1.:   
                self.NESW_win1 = self.NESW_win1 + 1
            else:
                self.NESW_win2 = self.NESW_win2 + 1
            if x == len(self.board) or y == -1:
                break




    def easy_AI(self):
        #The easy ai will randomly chose a location
        temp = random.randint(0,len(self.board)-1)
        return temp
    
    def med_AI(self):
        #the medium ai will place tokens next to his own most of the time
        if self.AImode == -1:
            self.AImode = random.randint(0,3)
            temp = random.randint(0,len(self.board)-1)
            return temp        
        empt = boa.check(self.PP_P2,0.)
        if len(empt[self.AImode]) == 0:
            self.AImode = random.randint(0,3)
            boa.med_AI()
        a = empt[self.AImode]
        b = a[random.randint(0,len(empt[self.AImode])-1)]
        return b[0]
    
    
    def hard_AI(self):
        #the hard ai will place tokens next to his own most of the time and try to block the opponents winning moves
        if self.AImode == -1:
            self.AImode = random.randint(0,3)
            temp = random.randint(0,len(self.board)-1)
            return temp
           
        empt = boa.check(self.PP_P1,0.)
        empt1 = boa.check(self.PP_P2,0.)


        #checks if player one is about to win
        boa.check_NS(self.PP_P1,1.)
        boa.check_win()
        boa.check_WE(self.PP_P1,1.)
        boa.check_win()
        boa.check_NWSE(self.PP_P1,1.)   
        boa.check_win()
        boa.check_NESW(self.PP_P1,1.)
        boa.check_win()
        
        #if player 1 is about to win it will try to place it next to player 1 last location to block
        if (self.NS_win1 == (self.winNum -1)) and empt[0] != 0:
            a = empt[0]
            b = a[random.randint(0,len(empt[self.AImode])-1)]
            return b[0]
            
        if (self.WE_win1 == (self.winNum -1)) and empt[1] != 0:
            a = empt[1]
            b = a[random.randint(0,len(empt[self.AImode])-1)]
            return b[0]
            
        if (self.NWSE_win1 == (self.winNum -1)) and empt[2] != 0:
            a = empt[2]
            b = a[random.randint(0,len(empt[self.AImode])-1)]
            return b[0]
            
        if (self.NESW_win1 == (self.winNum -1)) and empt[3] != 0 :
            a = empt[3]
            b = a[random.randint(0,len(empt[self.AImode])-1)]
            return b[0]
            
        if len(empt1[self.AImode]) == 0:
            self.AImode = random.randint(0,3)
            boa.med_AI()
            
            
        a = empt1[self.AImode]
        b = a[random.randint(0,len(empt1[self.AImode])-1)]
        
        return b[0]
        
        
        
        
        
        
        
            
        
   
def userplace():
    while  True:
            try:
                location = int(input("collum: "))
                if location in range(0,len(boa.board)):
                    break
                else:
                    print("NO you cannot place there, the column does not exist")
            except:
                print("Enter INT")
                userplace() 
    
    
    
    temp = boa.place(location,1.)
    if temp == True :
        userplace() 
    else:
        boa.check_NS(temp,1.)
        a = boa.check_win()
        boa.check_WE(temp,1.)
        b = boa.check_win()
        boa.check_NWSE(temp,1.)
        c = boa.check_win()    
        boa.check_NESW(temp,1.)
        d = boa.check_win()
        return a,b,c,d
    
    

def computerplace(mode):
    if mode == "e":
        location = boa.easy_AI()
    elif mode == "m":
        location = boa.med_AI()
    elif mode == "h":
        location = boa.hard_AI()
    else:
        while  True:
            try:
                location = int(input("collum: "))
                if location in range(0,len(boa.board)):
                    break
                
                else: 
                    print("NO you cannot place there, the column does not exist")
            except:
                print("Enter INT")
                computerplace(mode) 
                
                
    temp = boa.place(location,2.)
    
    
    if temp == True :
        computerplace(mode)
    else:
        boa.check_NS(temp,2.)
        a = boa.check_win()
        boa.check_WE(temp,2.)
        b = boa.check_win()
        boa.check_NWSE(temp,2.)
        c = boa.check_win()    
        boa.check_NESW(temp,2.)
        d = boa.check_win()
        #print(a,b,c,d,"|",temp)
        return a,b,c,d



def main():
    userInput = input("would you like to play? ")
    if (userInput.lower() == "y") or (userInput.lower() == "yes"):
        print("Starting")
    else:
        print("unknown input, quit?")
        userInput = input("would you like to quit? ")
        if userInput.lower() == ("y" or "yes"):
            return
        else:
            main()
    mode = input("""Pick AI mode:
easy: e  medium: m  hard: h  manual: anything
""")
    print("using ai: ",mode)
    
    while  True:
        try:
            w = int(input("w: "))
            h = int(input("h: "))
            
            wn = int(input("In a row number: "))
            break
        except:
            print("Enter INT")
    
    global boa
    boa = GB(h,w)
    boa.winNUM = wn
    boa.display()
    while True:
        

        print(boa)
        a , b, c, d = userplace()
        boa.display()
        if a or b or c or d:
            print("GAME OVER")
            break
        elif (len(boa.x0) == 0):
            print("its a tie")
            print("GAME OVER")
            break
        
        a,b,c,d = computerplace(mode)

        boa.display()
        #check for game over and or tie
        if a or b or c or d:
            print("GAME OVER")
            break
        elif (len(boa.x0) == 0):
            print("its a tie")
            print("GAME OVER")
            break
        
        
        
        



main()