from Tkinter import *
from random import randrange,random
from time import sleep
import sys

class Player:
    def __init__(self, bossNumber ,speed):
        self.bossNumber = bossNumber;
        self.speed = speed
        self.length = self.width = bossNumber * 50              #the size of the board
        self.root = Tk()
        self.bindKeys()
        self.root.title('line game')
        self.canvas = Canvas(self.root, width = self.length+20, height = self.width+20, bg='white')
        self.canvas.pack()
        self.canvas.create_rectangle(10,10,self.length+10,self.width+10,fill='gray',outline='gray')
        self.player = self.canvas.create_rectangle(5,5,10,10,outline='red',fill='red')
        self.mutex = True

        self.bossBox = []                                       #the boss's [id,positionX,positionY,direction]
        self.isAlive = True                                     #is the player alive
        self.newLine = []                                       #the new line that the player is drawing
        self.newPoint = []                                      #id of points in the new line
        self.occupy = 0                                         #the number of points that have been occupied
        self.x = self.y = 1                                     #player's position
        self.clean = []                                         #used to clean up
        self.point = []                                         #the state of every point in the board
                                                                    #if a point is occupied,then self.point[y][x] = 0
                                                                    #if a point is blank,then self.point[y][x] = 1
                                                                    #if a point is in newLine,then self.point[y][x] = 2
                                                                    #if a point is with a boss,then self.point[y][x] = 3
        for y in range(0,(self.length+20)/5):
            self.point.append([])
            self.clean.append([])
            for x in range(0,(self.width+20)/5):
                self.point[y].append(0)
                self.clean[y].append(False)
        for y in range(2,(self.length+10)/5):
            for x in range(2,(self.width+10)/5):
                self.point[y][x] = 1
    def start(self):
        for i in range(self.bossNumber):
            self.createBoss()
        while(True):
            for bossInfor in self.bossBox:
                bossInfor[1],bossInfor[2],bossInfor[3] = self.bossMove(bossInfor)
            if self.isAlive==False or self.occupy>self.length*self.width/50:
                if self.isAlive:    winner = 'You'
                else:   winner = 'Boss'
                quitButton = Button(self.root,text='%s win.You can click me to quit'%winner,command=self.root.quit)
                quitButton.pack()
                break
        self.root.mainloop()
        self.root.destroy()
    def createBoss(self):
        x = randrange(3,self.length/5+2)
        y = randrange(3,self.width/5+2)
        direction = ['u','d','l','r','ul','ur','dr','dl','ul','ur','dr','dl','ul','ur','dr','dl'][randrange(0,16)]
        boss = self.canvas.create_rectangle(x*5,y*5,x*5+5,y*5+5,outline='blue',fill='blue')
        self.bossBox.append([boss,x,y,direction])
    def bossMove(self,bossInfo):
        sleep(0.1/self.bossNumber/self.speed)
        boss,x,y,direction = bossInfo
        dx = dy = 0
        if(direction=='u'):
            if(self.point[y-1][x]==0):
                direction='d'
            else:
                dy = -1
        elif(direction=='d'):
            if(self.point[y+1][x]==0):
                direction = 'u'
            else:
                dy = 1
        elif(direction=='l'):
            if(self.point[y][x-1]==0):
                direction = 'r'
            else:
                dx = -1
        elif(direction=='r'):
            if(self.point[y][x+1]==0):
                direction = 'l'
            else:
                dx = 1
        elif(direction=='ul'):
            if(self.point[y-1][x-1]==0):
                if(self.point[y][x-1]==0 and self.point[y-1][x]==0):
                    direction = 'dr'
                elif(self.point[y][x-1]==0):
                    direction = 'ur'
                elif(self.point[y-1][x]==0):
                    direction = 'dl'
                else:
                    direction = 'dr'
            else:
                dx = dy = -1
        elif(direction=='ur'):
            if(self.point[y-1][x+1]==0):
                if(self.point[y][x+1]==0 and self.point[y-1][x]==0):
                    direction = 'dl'
                elif(self.point[y][x+1]==0):
                    direction = 'ul'
                elif(self.point[y-1][x]==0):
                    direction = 'dr'
                else:
                    direction = 'dl'
            else:
                dx = 1
                dy = -1
        elif(direction=='dl'):
            if(self.point[y+1][x-1]==0):
                if(self.point[y][x-1]==0 and self.point[y+1][x]==0):
                    direction = 'ur'
                elif(self.point[y][x-1]==0):
                    direction = 'dr'
                elif(self.point[y+1][x]==0):
                    direction = 'ul'
                else:
                    direction = 'ur'
            else:
                dx = -1
                dy = 1
        elif(direction=='dr'):
            if(self.point[y+1][x+1]==0):
                if(self.point[y][x+1]==0 and self.point[y+1][x]==0):
                    direction = 'ul'
                elif(self.point[y][x+1]==0):
                    direction = 'dl'
                elif(self.point[y+1][x]==0):
                    direction = 'ur'
                else:
                    direction = 'ul'
            else:
                dx = dy = 1
        else:
            raise ValueError('the direction of boss is wrong')
        self.canvas.move(boss,dx*5,dy*5)
        self.canvas.update()
        x += dx
        y += dy
        if (self.point[y][x]==2):
            self.isAlive = False
        self.point[y][x] = 3
        if dx!=0 or dy!=0:
            self.point[y-dy][x-dx] = 1
        return x,y,direction
    def bindKeys(self):
        self.root.bind('<Key-A>',self.moveLeft)
        self.root.bind('<Key-W>',self.moveUp)
        self.root.bind('<Key-S>',self.moveDown)
        self.root.bind('<Key-D>',self.moveRight)
        self.root.bind('<Key-a>',self.moveLeft)
        self.root.bind('<Key-w>',self.moveUp)
        self.root.bind('<Key-s>',self.moveDown)
        self.root.bind('<Key-d>',self.moveRight)
        self.root.bind('<Key-Left>',self.moveLeft)
        self.root.bind('<Key-Up>',self.moveUp)
        self.root.bind('<Key-Down>',self.moveDown)
        self.root.bind('<Key-Right>',self.moveRight)
    def moveNext(self,dx,dy):
        if(self.mutex == False):
            return
        self.mutex = False
        if(self.x+dx>=1 and self.x+dx<=self.length/5+2 and self.y+dy>=1 and self.y+dy<=self.width/5+2):            #start or continue to draw a line
            if(self.point[self.y+dy][self.x+dx] == 1):
                point = self.canvas.create_rectangle(self.x*5+dx*5,self.y*5+dy*5,self.x*5+dx*5+5,self.y*5+dy*5+5,outline='white')
                self.newPoint.append(point)
                self.newLine.append((self.x+dx,self.y+dy))
                self.point[self.y+dy][self.x+dx] = 2
            #call back a line(the next point is in trace already)
            elif(self.point[self.y+dy][self.x+dx] == 2):
                mid = self.newLine.index((self.x+dx,self.y+dy))
                for i in self.newPoint[mid+1:]:
                    self.canvas.delete(i)
                for j in self.newLine[mid+1:]:
                    self.point[j[1]][j[0]] = 1
                self.newPoint = self.newPoint[:mid+1]
                self.newLine = self.newLine[:mid+1]
            #draw a line successfully
            elif(self.point[self.y][self.x]==2 and self.point[self.y+dy][self.x+dx]==0):
                if(len(self.newLine)!=1):
                    for i in self.newLine:
                        self.point[i[1]][i[0]] = 0
                        self.occupy += 1
                        self.canvas.create_rectangle(i[0]*5,i[1]*5,i[0]*5+5,i[1]*5+5,outline='white',fill='white')
                    self.cleanUp()
                else:
                    self.point[self.newLine[0][1]][self.newLine[0][0]] = 1
                    self.canvas.delete(self.newPoint[0])
                self.newLine = []
                self.newPoint = []
                self.canvas.delete(self.player)
                self.player = self.canvas.create_rectangle(self.x*5,self.y*5,self.x*5+5,self.y*5+5,outline='red',fill='red')
            elif(self.point[self.y+dy][self.x+dx]==3):
                self.isAlive = False
            #change the position of player
            self.canvas.move(self.player,dx*5,dy*5)
            self.canvas.update()
            self.x += dx
            self.y += dy
        self.mutex = True
    def cleanUp(self):
        for y in range(2,self.length/5+2):
            for x in range(2,self.width/5+2):
                if(self.dfs(x,y)==False):
                    self.change(x,y)
        for y in range(2,self.length/5+2):
            for x in range(2,self.width/5+2):
                self.clean[y][x] = False
    def dfs(self,x,y):
        if(self.clean[y][x]==True):return True
        self.clean[y][x] = True
        if(self.point[y][x]==0):return True
        result = self.point[y][x] == 3
        if(x+1<self.width/5+3 and self.clean[y][x+1]==False and self.point[y][x+1]!=0):
            result = self.dfs(x+1,y) or result
        if(y+1<self.length/5+3 and self.clean[y+1][x]==False and self.point[y+1][x]!=0):
            result = self.dfs(x,y+1) or result
        if(x-1 > 1 and self.clean[y][x-1]==False and self.point[y][x-1]!=0):
            result = self.dfs(x-1,y) or result
        if(y-1 > 1 and self.clean[y-1][x]==False and self.point[y-1][x]!=0):
            result = self.dfs(x,y-1) or result
        return result
    def change(self,x,y):
        if(self.point[y][x]!=0):
            self.point[y][x] = 0
            self.canvas.create_rectangle(x*5,y*5,x*5+5,y*5+5,outline='white',fill='white')
            self.occupy += 1
            self.canvas.create_rectangle(x*5,y*5,x*5+5,y*5+5,outline='white')
            if(self.point[y+1][x]!=0):self.change(x,y+1)
            if(self.point[y-1][x]!=0):self.change(x,y-1)
            if(self.point[y][x+1]!=0):self.change(x+1,y)
            if(self.point[y][x-1]!=0):self.change(x-1,y)
    def moveLeft(self,event):
        self.moveNext(-1,0)
    def moveRight(self,event):
        self.moveNext(1,0)
    def moveUp(self,event):
        self.moveNext(0,-1)
    def moveDown(self,event):
        self.moveNext(0,1)
    
    



def main():
    sys.setrecursionlimit(10000)
    player = Player(5,3)
    player.start()
if __name__ == '__main__':
    main()
