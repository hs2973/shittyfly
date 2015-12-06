import math, os

path = os.getcwd()

class Utilities(self):
    def gradient(x1,y1,x2,y2):
        slope = ((y2-y1)/float(x2-x1))
        print(slope)
        return slope

class Sticky:
    def __init__(self,x,y,a):
        self.x = x # x-cordinatie of top-left point
        self.y = y # y-cordinatie of top-left point
        self.a = a # width of the sticky
        
    def display(self):
        rect(self.x,self.y,self.a,self.a)
    
class Poo:
    def __init__(self,x,y,a):
        self.x = x
        self.y = y
        self.a = a
    
    def display(self):
        ellipse(self.x,self.y,self.a,self.a)

class Fly:
    def __init__(self,x,y,a):
        self.x = x
        self.y = y
        self.a = a
        self.vx = 3
        self.vy = 3
        
        self.pointsCrossed = 0
        self.pathGradients = []
        
        self.speedChange = "increase"
    
    def display(self):
        ellipse(self.x,self.y,self.a,self.a)
        
    def calculateGradients(self):
        for i in range(len(game.points)-1):
            point1 = game.points[i]
            point2 = game.points[i+1]
            print(point1, point2)
            self.pathGradients.append(gradient(point1[0],point1[1],point2[0],point2[1]))
    
    def calculateMilestones(self):
        for i in range(len(game.points)-1):
            point1 = game.points[i]
            point2 = game.points[i+1]
            
            self.milestones.append(math.sqrt(abs(point2[0]-point1[0])**2+abs(point2[1]-point1[1])**2)//3)
            
        
class Game:
    def __init__(self,w,h,a): #width, height, thickness
        self.w = w
        self.h = h
        self.a = a
        
        self.state = "deploy"
        self.level = 1
     
        self.pointsLimit = 4
        self.points = []
        self.stickies = []
        
        #Poo and Housefly markers
        self.margin = 50
        self.flyThickness = 60
        self.fly = Fly(self.w-(self.margin+self.flyThickness/2),self.h-(self.margin+self.flyThickness/2),self.flyThickness)
        self.pooThickness = 100
        self.poo = Poo(self.margin+self.pooThickness/2,self.margin+self.pooThickness/2,self.pooThickness)
        
        #Adding the centre of Housefly as first point in the Points List
        self.points.append([self.w-(self.margin+self.flyThickness/2),self.h-(self.margin+self.flyThickness/2)])
        
        self.loadData()
                 
        #minimum distance from the mouse pointer for the circle dot to show
        self.minDistance = 5
    
    def loadData(self):
        #points = open(path+'/points'+str(self.level)+".txt")
        #for point in points:
        #    cords = point.strip().split(',')
        #    self.points.append([int(cords[0]),int(cords[1])])
        
        #points.close()
            
        stickies = open(path+'/stickies'+str(self.level)+".txt")
        for sticky in stickies:
            cords = sticky.strip().split(',')
            self.stickies.append([int(cords[0]),int(cords[1])])
        
    def printBoard(self):
        background(255)
        stroke(238,238,238)
        
        #Horizontal and Vertical gridlines
        for i in range(self.a,self.w,self.a):
            line(i, 0, i, self.h)
            
        for i in range(self.a,self.h,self.a):
            line(0, i, self.w, i)
    
    def printMarkers(self):
        self.printBoard()
        
        self.fly.display()
        self.poo.display()
        
        fill(255,0,0) #RED color pointer
        for point in self.points:
            ellipse(point[0],point[1], 10, 10)
            
        fill(0,255,0)
        for cords in self.stickies:
            rect(cords[0],cords[1], game.a, game.a)
        
        stroke(100,100,100)
        for i in range(len(self.points)-1):
            line(self.points[i][0], self.points[i][1], self.points[i+1][0], self.points[i+1][1])
    
    def deploy(self):
        self.printMarkers()
        
        if(len(game.points)<=game.pointsLimit):
            distance, nearestCords = self.getNearestCords()
            
            if(distance <= self.minDistance):
                ellipse(nearestCords[0],nearestCords[1], 10, 10)
                cursor(HAND)
            else:
                cursor(ARROW)
        else:
            cursor(ARROW)
            game.state = "follow"
            if len(self.fly.pathGradients) == 0:
                self.fly.calculateGradients()
                #self.fly.calculateMilestones()
                print(self.fly.pathGradients)
    
    def follow(self):
        self.printMarkers()
        
        for sticky in self.stickies:
            if(self.flyCollides(sticky)):
                print("Collision")
                return False

        if self.fly.pointsCrossed < len(self.points)-1:
            #print(self.fly.pathGradients)
            incrementX = abs(math.cos(math.atan(self.fly.pathGradients[self.fly.pointsCrossed])) * self.fly.vx)
            incrementY = abs(math.sin(math.atan(self.fly.pathGradients[self.fly.pointsCrossed])) * self.fly.vy)
            
            x2minusx1 = game.points[self.fly.pointsCrossed+1][0]-game.points[self.fly.pointsCrossed][0]
            y2minusy1 = game.points[self.fly.pointsCrossed+1][1]-game.points[self.fly.pointsCrossed][1]
            self.fly.x += x2minusx1/abs(x2minusx1)*incrementX
            self.fly.y += y2minusy1/abs(y2minusy1)*incrementY
            
            if self.fly.speedChange == "increase":
                self.fly.vx += 0.2
                self.fly.vy += 0.2
            elif self.fly.speedChange == "decrease":
                self.fly.vx -= 0.8
                self.fly.vy -= 0.8
            
            decreaseSpeed = False
            
            if x2minusx1 > 0:
                if y2minusy1 > 0:
                    if self.fly.x >= game.points[self.fly.pointsCrossed+1][0] and self.fly.y >= game.points[self.fly.pointsCrossed+1][1]:
                        decreaseSpeed = True
                else:
                    if self.fly.x >= game.points[self.fly.pointsCrossed+1][0] and self.fly.y <= game.points[self.fly.pointsCrossed+1][1]:
                        decreaseSpeed = True
            else:
                if y2minusy1 > 0:
                    if self.fly.x <= game.points[self.fly.pointsCrossed+1][0] and self.fly.y >= game.points[self.fly.pointsCrossed+1][1]:
                        decreaseSpeed = True
                else:
                    if self.fly.x <= game.points[self.fly.pointsCrossed+1][0] and self.fly.y <= game.points[self.fly.pointsCrossed+1][1]:
                        decreaseSpeed = True
                    
            if decreaseSpeed:
                self.fly.speedChange = "decrease"
            else:
                self.fly.speedChange = "increase"
                    
            if self.fly.speedChange == "decrease" and self.fly.vx <= 0:
                self.fly.speedChange = "increase"
                self.fly.pointsCrossed += 1
                self.fly.vx = 3
                self.fly.vy = 3
                
                if self.fly.pointsCrossed < len(self.fly.pathGradients):
                    game.points[self.fly.pointsCrossed][0] = self.fly.x
                    game.points[self.fly.pointsCrossed][1] = self.fly.y
                    self.fly.pathGradients[self.fly.pointsCrossed] = gradient(self.fly.x,self.fly.y,game.points[self.fly.pointsCrossed+1][0],game.points[self.fly.pointsCrossed+1][1])
                
                #self.fly.x = game.points[self.fly.pointsCrossed][0]
                #self.fly.y = game.points[self.fly.pointsCrossed][1]
            
            #self.fly.milestonesCount += 1
            
            #if(self.fly.milestonesCount >= self.fly.milestones[self.fly.pointsCrossed]):
            #    self.fly.pointsCrossed += 1
            #    self.fly.x = game.points[self.fly.pointsCrossed][0]
            #    self.fly.y = game.points[self.fly.pointsCrossed][1]
            #    self.fly.milestonesCount = 0
            #    print(self.fly.pointsCrossed)
            

            

    def getNearestCords(self):
        vectorList = [[0,0],[1,0],[1,1],[0,1]]
        squareCordsList = []
        
        #Left-top cords of the square
        cordX = (mouseX//self.a)*self.a
        cordY = (mouseY//self.a)*self.a
        
        for vector in vectorList:
            squareCordsList.append([cordX+vector[0]*self.a, cordY+vector[1]*self.a])
        
        distanceList = []
        for cord in squareCordsList:
            distanceList.append(math.sqrt(abs(cord[0]-mouseX)**2+abs(cord[1]-mouseY)**2))
        
        return min(distanceList),squareCordsList[distanceList.index(min(distanceList))]
    
    def flyCollides(self,sticky):
        stickyX = sticky[0] + self.a/2
        stickyY = sticky[1] + self.a/2
        circleDistanceX = abs(self.fly.x - stickyX)
        circleDistanceY = abs(self.fly.y - stickyY)
        
        if (circleDistanceX > (self.a/2 + self.fly.a/2)): return False
        if (circleDistanceY > (self.a/2 + self.fly.a/2)): return False
        
        if (circleDistanceX <= (self.a/2)): return True;  
        if (circleDistanceY <= (self.a/2)): return True; 
        
        cornerDistance_sq = (circleDistanceX - self.a/2)**2 + (circleDistanceY - self.a/2)**2
    
        return (cornerDistance_sq <= ((self.fly.a/2)**2));
        
        
        
game = Game(1200,760,20)
    
def setup():
    size(game.w, game.h)
    stroke(0)
    frameRate(20)
    game.printBoard()
    
def draw(): 
    if game.state == "deploy":
        game.deploy()
    elif game.state == "follow":
        game.follow()
    elif game.state == "gameover":
        print("Game Over")
    
def mousePressed():
    distance, nearestCords = game.getNearestCords()
    if(distance <= game.minDistance and len(game.points)<=game.pointsLimit):
        game.points.append(nearestCords)