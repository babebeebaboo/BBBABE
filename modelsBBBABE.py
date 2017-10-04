import arcade.key
import arcade
from random import randint
import math


class Model:
    def __init__(self,world,x,y,vx,vy,angle=0,hp=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.world = world
        self.angle = angle
        self.hp = hp

    def collision(self,other):
        
        down1 = ( (other.x - 29, other.y - 15),(other.x + 29, other.y - 15) , (other.x + 29, other.y-14), (other.x - 29, other.y-14))
        up1 = ( (other.x - 29, other.y + 15),(other.x + 29, other.y + 15) , (other.x + 29, other.y+16), (other.x - 29, other.y+16))
        left1 = ( (other.x - 30, other.y - 15),(other.x - 29, other.y -15) , (other.x - 29, other.y+15), (other.x - 30, other.y+15))
        right1 = ( (other.x + 29, other.y -15),(other.x + 30, other.y - 15), (other.x + 30, other.y+15), (other.x + 29, other.y+15))
        ball = ( (self.x - 10,self.y-10) , (self.x + 10,self.y- 10) , (self.x + 10,self.y+ 10) , (self.x - 10,self.y + 10))
        
        s = ""
        if arcade.are_polygons_intersecting(ball,down1) or arcade.are_polygons_intersecting(ball,up1):
            s += "y"
        if arcade.are_polygons_intersecting(ball,left1) or arcade.are_polygons_intersecting(ball,right1):
            s += "x"
        return s



    def hit(self,other):
        hit_sizeX = 30 + self.radius
        hit_sizeY = 15 + self.radius
        return (abs(self.x - other.x) <= hit_sizeX) and (abs(self.y - other.y) <= hit_sizeY)
        
    def ballHitBlock(self,other):
        DeltaX = self.x - max(other.x, min(self.x, other.x + other.width));
        DeltaY = self.y - max(other.y, min(self.y, other.y + other.height));
        return (DeltaX * DeltaX + DeltaY * DeltaY) < (self.radius * self.radius);


def GenerateBlock():
    return [[randint(0,9) for x in range(0,8)] for y in range(17)]

class Block(Model):
    def __init__(self,world,x,y,hp,width=60,height=30,vx=0,vy=0,angle=0):
        super().__init__(world,x,y,vx,vy,angle,hp)
        self.width = width
        self.height = height
        self.image = ""
        if hp == 1 :
            self.image = "images/block1.png"
        if hp == 2 :
            self.image = "images/block2.png"
        if hp == 3 :
            self.image = "images/block3.png"
        if hp == 4 :
            self.image = "images/block4.png"
        if hp == 5 :
            self.image = "images/block5.png"
        if hp == 6 :
            self.image = "images/block6.png"
        if hp == 7 :
            self.image = "images/block7.png"
        if hp == 8 :
            self.image = "images/block8.png"
            
        if hp == 9 :
            self.image = "images/block+.png"
            
    def update(self,delta):
        pass

class Arrow(Model):
    def __init__(self,world,x,y,vx,vy,angle,move=1):
        super().__init__(world,x,y,vx,vy,angle)
        self.move = move
    def update(self,delta):
        
        self.angle += self.move 
        if self.angle <= 0+5 or self.angle >= 180-5: 
            self.move *= 0
       # print(self.angle)

class Ball(Model):
    def __init__(self,world,x,y,vx,vy,size,running = False):
        super().__init__(world,x,y,vx,vy)
        self.size = size
        self.radius = size/2
        self.running = False

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

    def update(self,delta):
        
        if (self.x < self.radius) or (self.x > self.world.width-self.radius):
            self.vx = - self.vx
        
        if (self.y < self.radius) or (self.y > self.world.height-self.radius):
            self.vy = - self.vy

        self.x += self.vx
        self.y += self.vy

        if self.y < 20 :
            if self.x < self.radius:
                self.x = self.radius
            if self.x > 600 - self.radius:
                self.x = 600 - self.radius
            
            self.y = 20
            self.vx = 0
            self.vy = 0
            self.running = False
            
        if not self.running :
            return self.x
        else :
            return -1
        
class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.ball = Ball(self,300,20,0,0,20)
        self.arrow = Arrow(self,300,20,0,0,179-5,0)
        self.blockshp = GenerateBlock()
        self.blocks = []
        self.breakBlock =0
        self.score = 0
        for j in range(0,8):
            for i in range(0,16):
                if self.blockshp[i][j] > 0 :
                    block = Block(self,j*60+30+60,i*30+15 +270,self.blockshp[i][j])
                    
                    self.blocks.append(block)
        self.noOfBlock = len( self.blocks)
        
    def on_key_press(self, key, key_modifiers):
        
        if key == arcade.key.SPACE and self.ball.running == False:
            self.ball.shoot(self.arrow.angle)
            print ("SPACE "+"VX = "+ str(self.ball.vx) + " VY = "+str(self.ball.vy) )
            self.score += 1
        
        if key == arcade.key.LEFT:
            self.arrow.move = 1
        if key == arcade.key.RIGHT:
            self.arrow.move = -1

    def on_key_release(self, key, key_modifiers):
        if not key == arcade.key.LEFT:
            self.arrow.move = 0
        if not key == arcade.key.RIGHT:
            self.arrow.move = 0
        
    def update(self,delta):
        
        arrowPlace = self.ball.update(delta)
        if arrowPlace != -1:
            self.arrow.x = arrowPlace
        self.arrow.update(delta)
        hit=0
        changeX=0
        changeY=0
        collision = 0
        
        for block in self.blocks:
            block.update(delta)

            collision = self.ball.collision(block)
            if collision :
                if collision == "y":
                    changeY += 1
                if collision == "x":
                    changeX += 1
                if len(collision) > 1:
                    if abs(self.ball.vx) > abs(self.ball.vy):
                        changeX += 1
                    if abs(self.ball.vy) > abs(self.ball.vx):
                        changeY += 1
                print ( "X "+"Ball: "+str(self.ball.x) + " "+"Block: "+str(block.x) +" "+"Range: "+ str( abs(block.x - self.ball.x) ) )
                print( "Y "+"Ball: "+str(self.ball.y) + " "+"Block: "+str(block.y)+" "+"Range: "+ str( abs(block.y - self.ball.y) ) )
                print(collision +  " Block HP : "+str(block.hp) + " Score = " + str(self.score))
                hit+=1
                block.hp -= 1
                if block.hp <=0:
                    block.y=-100
                    block.x=-100
                    self.breakBlock += 1
        if hit>0:
            if changeX >0:
                self.ball.vx *= -1
                
            if changeY >0:
                self.ball.vy *= -1
            print ("VX = "+ str(self.ball.vx) + " VY = "+str(self.ball.vy) )
            print()