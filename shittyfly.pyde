add_library('minim')
minim = Minim(this)
import math, os
path = os.getcwd()

class Utilities:
    def gradient(self,x1,y1,x2,y2):
        if float(x2-x1) == 0:
            slope = 999999999
        else:
            slope = ((y2-y1)/float(x2-x1))
        print(slope)
        return slope
    
    def intersects(self,circle,rectangle):
        # Get the centre of the rectangle
        rectangleX = rectangle.x + rectangle.w/2
        rectangleY = rectangle.y + rectangle.h/2
        
        circleDistanceX = abs(circle.x - rectangleX)
        circleDistanceY = abs(circle.y - rectangleY)
        
        if (circleDistanceX > (rectangle.w/2 + circle.r)): return False
        if (circleDistanceY > (rectangle.h/2 + circle.r)): return False
        
        if (circleDistanceX <= (rectangle.w/2)): return True  
        if (circleDistanceY <= (rectangle.h/2)): return True
        
        cornerDistance_sq = (circleDistanceX - rectangle.w/2)**2 + (circleDistanceY - rectangle.h/2)**2
    
        return (cornerDistance_sq <= (circle.r**2))
    
    def outOfBounds(self, circle):
        circleDistanceX = abs(circle.x + circle.r)
        circleDistanceY = abs(circle.y + circle.r)
        if 0 >= circle.x-circle.r or circleDistanceX >= game.w:
            return False
        elif 0 >= circle.y-circle.r or circleDistanceY >= game.h:
            return False
        else:
            return True

utilities = Utilities()

class Point:
    def __init__(self,x,y): # x and y coordinates
        self.x = x
        self.y = y
        self.r = 5
        
        self.imgSmell = loadImage(path + "/images/smellSprite.png")
        self.frame = 0
        self.frames = 5
        self.frameWidth = self.imgSmell.width/self.frames
        self.frameHeight = self.imgSmell.height
        
    def display(self):
        fill(0,255,0) 
        
        if self.frame == self.frames-1:
            self.frame = 0
        else:
            self.frame += 1
            
        image(self.imgSmell,self.x-(self.frameWidth/2),self.y-(self.frameHeight),self.frameWidth,self.frameHeight,self.frame*self.frameWidth,0,(self.frame+1)*self.frameWidth,self.frameHeight)

        ellipse(self.x,self.y,2*self.r,2*self.r) 

class Sticky:
    def __init__(self,x,y,a):
        self.x = x # x-cordinatie of top-left point
        self.y = y # y-cordinatie of top-left point
        self.a = a # width of the sticky
        self.imgPath = path + "/images/sticky.png"
        
        self.img = loadImage(self.imgPath)
        
        # width and height defined for purpose of collision
        self.w = a
        self.h = a
        
    def display(self):
        fill(0,255,0)
        image(self.img,self.x,self.y)

class Poo:
    def __init__(self,x,y,w,h):
        self.x = x+50
        self.y = y+50
        self.w = w
        self.h = h
        
        self.moonImg = loadImage(path + "/images/full-moon.png")
        self.moonImg.resize(140,140)
        
        self.img = loadImage(path + "/images/poo.png")
        self.img.resize(80,60)
    
    def display(self):
        noFill()
        stroke(255,0,0)
        centerX = self.x+self.img.width/2
        centerY = self.y+self.img.height/2
        image(self.moonImg, centerX - self.moonImg.width/2, centerY - self.moonImg.height/2)
        #ellipse(self.x+self.img.width/2,self.y+self.img.height/2+5,90,90)
        image(self.img, self.x, self.y)
        
    def intersects(self,circle):
        centerX = self.x+self.img.width/2
        centerY = self.y+self.img.height/2
        
        circleDistanceX = abs(centerX - circle.x)
        circleDistanceY = abs(centerY - circle.y)
        
        distance = (circleDistanceX**2 + circleDistanceY**2)**0.5
        
        if (distance <= (self.moonImg.width/2 + circle.r - 10)): 
            return True
        else:
            return False
        
class Fly:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 3
        self.vy = 3
        self.lastV = -1
        
        self.img = loadImage(path + "/images/flySprite.png")
        self.imgR = loadImage(path + "/images/flySpriteR.png")
        self.frame = 0
        self.frames = 6
        self.frameWidth = self.img.width/self.frames
        self.frameHeight = self.img.height
        
        self.imgDead = loadImage(path + "/images/flyDead.png")
        self.imgDeadR = loadImage(path + "/images/flyDeadR.png")
        
        self.pointsCrossed = 0
        self.pathGradients = []
        
        self.speedChange = "increase"
    
    def display(self):
        noFill()
        stroke(0,255,0)
        ellipse(self.x,self.y,2*self.r,2*self.r)
        noStroke()
        
        if game.state == "gameover":
            if self.lastV == 1:
                image(self.imgDeadR,self.x-self.r-15,self.y-self.r-10)
            else:
                image(self.imgDead,self.x-self.r-15,self.y-self.r-10)
        else:
            if self.frame == self.frames-1:
                self.frame = 0
            else:
                self.frame += 1
                
            if self.lastV == 1:
                image(self.imgR,self.x-self.r-15,self.y-self.r-10,self.frameWidth,self.frameHeight,self.frame*self.frameWidth,0,(self.frame+1)*self.frameWidth,self.frameHeight)
            else:
                image(self.img,self.x-self.r-15,self.y-self.r-10,self.frameWidth,self.frameHeight,self.frame*self.frameWidth,0,(self.frame+1)*self.frameWidth,self.frameHeight)
        
        
            
    def calculateGradients(self):
        for i in range(len(game.points)-1):
            point1 = game.points[i]
            point2 = game.points[i+1]
            print(point1, point2)
            self.pathGradients.append(utilities.gradient(point1.x,point1.y,point2.x,point2.y))
        
class Game:
    def __init__(self,w,h,a): #width, height, thickness for the grid
        self.w = w
        self.h = h
        self.a = a
        
        self.state = "menu"
        self.level = 1
        
        self.music = minim.loadFile(path + "/music/moon.mp3")
        
        # Number of points (smells) allowed
        self.pointsLimit = 4
        self.points = []
        
        self.stickies = []
        
        # Margin for the fly and poo markers
        self.margin = 50
        
        # Poo and Housefly markers
        self.flyRadius = 25
        self.fly = Fly(self.w-(self.margin+self.flyRadius),self.h-(self.margin+self.flyRadius),self.flyRadius)
        self.poo = Poo(self.margin,self.margin,self.a*4,self.a*3)
        
        # Adding the centre of Housefly as first point in the Points List
        self.points.append(Point(self.w-(self.margin+self.flyRadius),self.h-(self.margin+self.flyRadius)))
        
        # Load stickies data
        self.loadData()
                 
        # Minimum distance (in pixels) from the mouse pointer for the circle dot to show
        self.minDistance = 5
        
        self.backgroundImg = loadImage(path+"/images/sky.jpg")
        self.backgroundImg.resize(self.w,self.h)
        
    def reset(self, nextState):
        self.fly = Fly(self.w-(self.margin+self.flyRadius),self.h-(self.margin+self.flyRadius),self.flyRadius)
        self.points=[]
        self.points.append(Point(self.w-(self.margin+self.flyRadius),self.h-(self.margin+self.flyRadius)))
        self.poo = Poo(self.margin,self.margin,self.a*4,self.a*3)
        self.state = nextState
        self.stickies = []
        self.loadData()
    
    def loadData(self):  
        stickies = open(path+'/stickies'+str(self.level)+".txt")
        self.pointsLimit = int(stickies.readline())
        for sticky in stickies:
            cords = sticky.strip().split(',')
            self.stickies.append(Sticky(int(cords[0]),int(cords[1]),self.a))
        
    def printBoard(self):
        background(255)
        stroke(238,238,238)
        
        #image(self.backgroundImg,0,0)
        
        #noStroke()
        
        # Horizontal and Vertical gridlines
        for i in range(self.a,self.w,self.a):
            line(i, 0, i, self.h)
            
        for i in range(self.a,self.h,self.a):
            line(0, i, self.w, i)
            
    def printMarkers(self):
        self.printBoard()
        
        textSize(20)
        s = "Smells left:" + str(self.pointsLimit - len(self.points)+1)
        text(s, 950, 50)
            
        for sticky in self.stickies:
            sticky.display()
   
        for point in self.points:
            point.display()
        
        stroke(255,0,0)
        for i in range(len(self.points)-1):
            line(self.points[i].x, self.points[i].y, self.points[i+1].x, self.points[i+1].y)
        
        self.poo.display()
        self.fly.display()
        
    def deploy(self):
        self.printMarkers()
        fill(255,0,0)
        
        if(len(game.points)<=game.pointsLimit):
            distance, nearestCords = self.getNearestCords()
            
            if(distance <= self.minDistance):
                ellipse(nearestCords[0],nearestCords[1], 10, 10)
                cursor(HAND)
            else:
                cursor(ARROW)
        else:
            cursor(ARROW)
            if len(game.fly.pathGradients) == 0:
                game.fly.calculateGradients()
            game.state = "follow"
            print(self.fly.pathGradients)
    
    def follow(self):
        self.printMarkers()
        
        if(self.poo.intersects(self.fly)):
            game.state = "gamewon"
            return False
            
        #if (utilities.outOfBounds(self.fly)) == False:
            #game.state = "gameover"
            #return False
        
        if self.fly.vx == 3 and self.fly.pointsCrossed >= len(self.points)-1:#Check whether fly stopped and it is over - then u lot. vx == 3 because of inital speed being 3
            game.state = "gameover"
            return False
        
        for sticky in self.stickies:
            if(utilities.intersects(self.fly,sticky)):
                game.state = "gameover"
                return False

        if self.fly.pointsCrossed < len(self.points)-1:
            incrementX = abs(math.cos(math.atan(self.fly.pathGradients[self.fly.pointsCrossed])) * self.fly.vx)
            incrementY = abs(math.sin(math.atan(self.fly.pathGradients[self.fly.pointsCrossed])) * self.fly.vy)
            
            x2minusx1 = game.points[self.fly.pointsCrossed+1].x-game.points[self.fly.pointsCrossed].x
            y2minusy1 = game.points[self.fly.pointsCrossed+1].y-game.points[self.fly.pointsCrossed].y
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
                self.fly.lastV=1
                if y2minusy1 > 0:
                    if self.fly.x >= game.points[self.fly.pointsCrossed+1].x and self.fly.y >= game.points[self.fly.pointsCrossed+1].y:
                        decreaseSpeed = True
                else:
                    if self.fly.x >= game.points[self.fly.pointsCrossed+1].x and self.fly.y <= game.points[self.fly.pointsCrossed+1].y:
                        decreaseSpeed = True
            else:
                self.fly.lastV=-1
                if y2minusy1 > 0:
                    if self.fly.x <= game.points[self.fly.pointsCrossed+1].x and self.fly.y >= game.points[self.fly.pointsCrossed+1].y:
                        decreaseSpeed = True
                else:
                    if self.fly.x <= game.points[self.fly.pointsCrossed+1].x and self.fly.y <= game.points[self.fly.pointsCrossed+1].y:
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
                    game.points[self.fly.pointsCrossed].x = self.fly.x
                    game.points[self.fly.pointsCrossed].y = self.fly.y
                    self.fly.pathGradients[self.fly.pointsCrossed] = utilities.gradient(self.fly.x,self.fly.y,game.points[self.fly.pointsCrossed+1].x,game.points[self.fly.pointsCrossed+1].y)
            
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
        
game = Game(1200,760,20)
    
def setup():
    size(game.w, game.h)
    stroke(0)
    frameRate(20)
    
    game.printBoard()
    
def draw(): 
    if game.state == "menu":
        background(255)
        fill(0)
        textSize(50)
        text("Menu", game.w/2-65, game.h/2)
        textSize(30)
        fill(255)
        rect(game.w/2-75, game.h/2+75,150,50)
        fill(0)
        text("Play", game.w/2-30, game.h/2+100)
        fill(255)
        rect(game.w/2-75, game.h/2+150,150,50)
        fill(0)
        text("Quit", game.w/2-30, game.h/2+175)
    elif game.state == "deploy":
        game.deploy()
        textSize(30) 
        noFill()
        stroke(255)
        text("Go!", 1100, 50)       
    elif game.state == "follow":
        game.follow()
    elif game.state == "gameover": #Gives the Game Over title if collision is detected
        game.printMarkers()
        print("Game Over")
        fill(0)
        textSize(50)
        text("GAME OVER", game.w/2-150, game.h/2)
        textSize(30)
        noFill()
        rect(game.w/2-75, game.h/2+75,150,50)
        fill(0)
        text("Try again", game.w/2-70, game.h/2+100)
        noFill()
        rect(game.w/2-95, game.h/2+150,190,50)
        fill(0)
        text("Go to menu", game.w/2-85, game.h/2+175)
    elif game.state == "gamewon":
        if game.level < 3:
            print("Game Won")
            fill(0)
            textSize(50)
            text("CONGRATULATIONS", game.w/2-250, game.h/2)
            textSize(30)
            fill(255)
            rect(game.w/2-75, game.h/2+75,150,50)
            fill(0)
            text("Next level", game.w/2-70, game.h/2+100)
            fill(255)
            rect(game.w/2-95, game.h/2+150,190,50)
            fill(0)
            text("Go to menu", game.w/2-85, game.h/2+175)
        else:
            fill(0)
            textSize(50)
            text("CONGRATULATIONS YOU WON", game.w/2-350, game.h/2)
            textSize(30)
            fill(255)
            rect(game.w/2-95, game.h/2+150,190,50)
            fill(0)
            text("Go to menu", game.w/2-85, game.h/2+175)
    
def mousePressed():
    distance, nearestCords = game.getNearestCords()
    if(distance <= game.minDistance and len(game.points)<=game.pointsLimit):
        game.points.append(Point(nearestCords[0], nearestCords[1]))
        
    if game.state == "menu":
        if game.w/2-75 <= mouseX <= game.w/2+75 and game.h/2+75 <= mouseY <= game.h/2+125: # From menu to starting game (PLAY!)
            game.music.play()
            game.reset("deploy")
        elif game.w/2-75 <= mouseX <= game.w/2+75 and game.h/2+150 <= mouseY <= game.h/2+200:
            print("quit")
            exit()
            
    elif game.state == "deploy":
        if 1075<=mouseX<=game.w and 22<=mouseY<=60:
            if len(game.fly.pathGradients) == 0:
                game.fly.calculateGradients()
            game.state = "follow"
            
        
    elif game.state == "gameover":
        if game.w/2-75 <= mouseX <= game.w/2+75 and game.h/2+75 <= mouseY <= game.h/2+125: # From game over to reseting the game (try again)
            game.reset("deploy")
            print(game.state)
        elif game.w/2-95 <= mouseX <= game.w/2+95 and game.h/2+150 <= mouseY <= game.h/2+200: # From game over screen to menu (Go to menu)
            background(255)
            game.reset("menu")
    
    elif game.state == "gamewon" and game.level < 3:
        if game.w/2-75 <= mouseX <= game.w/2+75 and game.h/2+75 <= mouseY <= game.h/2+125: # Going to next level(Next level)
            game.level = game.level+1
            game.reset("deploy")
            
            print(game.state)
            print(game.level)
        elif game.w/2-95 <= mouseX <= game.w/2+95 and game.h/2+150 <= mouseY <= game.h/2+200: # From game over screen to menu (Go to menu)
            background(255)
            game.reset("menu")
    elif game.state == "gamewon" and game.level >= 3:
        if game.w/2-95 <= mouseX <= game.w/2+95 and game.h/2+150 <= mouseY <= game.h/2+200: # From game over screen to menu (Go to menu)
            background(255)
            game.reset("menu")
        