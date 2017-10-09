import arcade.key
import arcade
from random import randint
import math

class Model:
    def __init__(self,world,x,y,vx=0,vy=0,angle=0,hp=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.world = world
        self.angle = angle
        self.hp = hp

def GenerateBlock():
    a = [[randint(0,8) for x in range(0,8)] for y in range(17)]
    a[randint(0,17)][randint(0,8)] = 9
    a[randint(0,17)][randint(0,8)] = 9
    a[randint(0,17)][randint(0,8)] = 9
    a[randint(0,17)][randint(0,8)] = 9
    a[randint(0,17)][randint(0,8)] = 9
    return a
    #return [[9 for x in range(0,8)] for y in range(17)]

class Block(Model):

    def changeImageByHp(self):
        image = "images/block"
        if self.hp <= 0 :
            image += "white"
        elif self.hp == 9 :
            image += "+"
        else :
            image += str(self.hp)
        image += ".png"        
        return image

    def __init__(self,world,x,y,hp,width=60,height=30,vx=0,vy=0,angle=0):
        super().__init__(world,x,y,vx,vy,angle,hp)
        self.width = width
        self.height = height
        self.image = self.changeImageByHp()

class Arrow(Model):
    def __init__(self,world,x,y,angle,vx=0,vy=0,move=1):
        super().__init__(world,x,y,vx,vy,angle)
        self.move = move
    def update(self,delta):
        self.angle += self.move 
        if self.angle <= 0+5 or self.angle >= 180-5: 
            self.move *= 0

class Ball(Model):
    def __init__(self,world,x,y,size,vx=0,vy=0,running = False):
        super().__init__(world,x,y,vx,vy)
        self.size = size
        self.radius = size/2
        self.running = running
        self.DefaultY = y

    def shoot(self,angle):
        self.running = True
        maxspeed = 20
        if angle == 180:
            angle -= 1
        if angle == 0:
            angle += 1
        self.vx = ( 90 - angle ) /90 *maxspeed
        if angle >=0 and angle <=90:
            self.vy = angle / 90 * maxspeed
        else :
            self.vy = (180 - angle) / 90 * maxspeed

    def update(self,world,delta):
        if self.y <= 20 and self.vy > 0:
            self.y += self.vy
            return -1

        if self.x < self.radius or self.x > self.world.width-self.radius:
            self.vx = - self.vx
        
        if self.y < self.radius or self.y > self.world.height-self.radius:
            self.vy = - self.vy

        self.x += self.vx
        self.y += self.vy

        if self.y < 20 and self.vy < 0:
            if world.ballX == -1:
                if self.x < self.radius:
                    self.x = self.radius
                if self.x > 600 - self.radius:
                    self.x = 600 - self.radius
            else:
                self.x = world.ballX
            
            self.y = self.DefaultY
            self.vx = 0
            self.vy = 0
            self.running = False
            
        if not self.running :
            if world.ballX == -1:
                world.ballX = self.x
            return self.x
        else :
            return -1

    def check_collision_list(self,world,list):
        hit=0
        changeX=0
        changeY=0
        breakblock=0
        for block in list:
            collision = self.collision(block)
            if collision :
                if collision == "y":
                    changeY += 1
                if collision == "x":
                    changeX += 1
                if len(collision) > 1:
                    if abs(self.vx) > abs(self.vy):
                        changeX += 1
                    if abs(self.vy) > abs(self.vx):
                        changeY += 1
                #print ( "X "+"Ball: "+str(self.x) + " "+"Block: "+str(block.x) +" "+"Range: "+ str( abs(block.x - self.x) ) )
                #print( "Y "+"Ball: "+str(self.y) + " "+"Block: "+str(block.y)+" "+"Range: "+ str( abs(block.y - self.y) ) )
                
                hit+=1
                block.hp -= 1

                if block.hp >= 8 :
                    block.hp = 0
                    world.noOfBall += 1
                    
                    ball = Ball(world,30, 19 - 50*(world.noOfBall-1) ,20)
                    world.balls.append(ball)
                    world.window.insert_ball(ball)

                if block.hp <= 0 :
                    block.y = -100
                    block.x = -100
                    breakblock += 1

        if hit>0:
            if changeX >0:
                self.vx *= -1
            if changeY >0:
                self.vy *= -1

            #print ("VX = "+ str(self.vx) + " VY = "+str(self.vy) +"\n")
        return breakblock

    def collision(self,other):
        down1 = ( (other.x - 29, other.y - 15),(other.x + 29, other.y - 15) , (other.x + 29, other.y-14), (other.x - 29, other.y-14))
        up1 = ( (other.x - 29, other.y + 15),(other.x + 29, other.y + 15) , (other.x + 29, other.y+16), (other.x - 29, other.y+16))
        left1 = ( (other.x - 30, other.y - 15),(other.x - 29, other.y -15) , (other.x - 29, other.y+15), (other.x - 30, other.y+15))
        right1 = ( (other.x + 29, other.y -15),(other.x + 30, other.y - 15), (other.x + 30, other.y+15), (other.x + 29, other.y+15))
        ball = ( (self.x - 10,self.y-10) , (self.x + 10,self.y- 10) , (self.x + 10,self.y+ 10) , (self.x - 10,self.y + 10))
        
        s = ""
        if arcade.are_polygons_intersecting(ball,down1) :
            self.y = other.y - (15 + self.radius + 1)
            s += "y"
        if arcade.are_polygons_intersecting(ball,up1) :
            self.y = other.y + (15 + self.radius + 1)
            if s == "":
                s += "y"
        if arcade.are_polygons_intersecting(ball,left1) :
            self.x = other.x - (30 + self.radius + 1)
            s += "x"
        if arcade.are_polygons_intersecting(ball,right1):
            self.x = other.x + (30 + self.radius + 1)
            if len(s) == 1:
                s += "x"

        return s

class World:
    def __init__(self,width,height,window):
        ''' Place everything on world except blocks '''
        self.width = width
        self.height = height
        self.window = window
        #self.ball = Ball(self,300,20,20)

        self.balls = []
        ball = Ball(self,300,20,20)
        self.balls.append(ball)
        self.ballX=-1

        self.arrow = Arrow(self,300,20,174)
        self.arrowPlace = -1
        ''' END Place everything on world except blocks '''
        ''' Generate Blocks '''
        self.blockshp = GenerateBlock()
        self.blocks = []
        for j in range(0,8):
            for i in range(0,16):
                if self.blockshp[i][j] > 0 :
                    block = Block(self,j*60+90,i*30+285,self.blockshp[i][j])
                    self.blocks.append(block)
        ''' END Generate Blocks '''
        ''' All about Score '''
        self.breakBlock =0
        self.score = 0
        self.noOfBlock = len(self.blocks)
        self.blockleft = self.noOfBlock - self.breakBlock
        self.noOfBall = 1
        ''' END All about Score '''
        
    def on_key_press(self, key, key_modifiers):
        
        if key == arcade.key.SPACE:
            print("aa")
            for ball in self.balls:
                if self.ballX != -1 :
                    ball.x = self.ballX
                if not ball.running:
                    ball.shoot(self.arrow.angle)
                    #print ("SPACE "+"VX = "+ str(ball.vx) + " VY = "+str(ball.vy) )
                    self.score += 1

            self.arrowPlace =-1
            self.ballX = -1

        if key == arcade.key.LEFT:
            self.arrow.move = 1
        if key == arcade.key.RIGHT:
            self.arrow.move = -1
        

    def on_key_release(self, key, key_modifiers):
        if not key == arcade.key.LEFT or not key == arcade.key.RIGHT:
            self.arrow.move = 0

        
    def update(self,delta):
        
        '''Block Ball'''
        for ball in self.balls:
            if not ball.running:
                continue
            k = ball.update(self,delta)
            if self.arrowPlace == -1:
                self.arrowPlace = k
                self.ballX = self.arrowPlace
            breakblock = ball.check_collision_list(self,self.blocks)
            if breakblock:
                self.breakBlock += breakblock
        self.blockleft = self.noOfBlock - self.breakBlock


        '''END Block Ball'''

        ''' Arrow '''
        if self.arrowPlace != -1:
            self.arrow.x = self.arrowPlace
        self.arrow.update(delta)
        '''END Arrow '''