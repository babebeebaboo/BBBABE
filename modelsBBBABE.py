import arcade.key
from random import randint

class Model:
    def __init__(self,world,x,y,vx,vy,angle=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.world = world
        self.angle = angle
    def hit(self,other,hit_sizeX,hit_sizeY):
        return (abs(self.x - other.x) <= hit_sizeX) and (abs(self.y - other.y) <= hit_sizeY)

def GenerateBlock():
    return [[randint(0,10) for x in range(0,8)] for y in range(17)]

class Block(Model):
    def __init__(self,world,x,y,hp,vx=0,vy=0,angle=0):
        super().__init__(world,x,y,vx,vy,angle)
        self.hp = hp
    def update(self,delta):
        pass

class Arrow(Model):
    def __init__(self,world,x,y,vx,vy,angle,move=1):
        super().__init__(world,x,y,vx,vy,angle)
        self.move = move
    def update(self,delta):
        self.angle += self.move
        if self.angle <= 0 or self.angle >= 180: 
            self.move *= -1
       # print(self.angle)
        

class Ball(Model):
    def __init__(self,world,x,y,vx,vy,size,running = False):
        super().__init__(world,x,y,vx,vy)
        self.size = size
        self.radius = size/2
        self.running = False

    def shoot(self,angle):
        self.running = True
        maxspeed = 10
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
            self.x = 300
            self.y = 20
            self.vx = 0
            self.vy = 0
            self.running = False

class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.ball = Ball(self,300,20,0,0,20)
        self.arrow = Arrow(self,300,20,0,0,179,1)
        self.blockshp = GenerateBlock()
        self.blocks = []
        self.score =0
        for j in range(0,8):
            for i in range(0,16):
                if self.blockshp[i][j] >0 :
                    block = Block(self,j*60+30+60,i*30+15 +270,self.blockshp[i][j])
                    self.blocks.append(block)
        self.noOfBlock = len( self.blocks)
        
        

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE and self.ball.running == False:
            self.ball.shoot(self.arrow.angle)
            
    def update(self,delta):
        self.ball.update(delta)
        self.arrow.update(delta)
        hit=0
        for block in self.blocks:
            block.update(delta)
            hitSizeX = 30 + self.ball.radius
            hitSizeY = 15 + self.ball.radius
            if self.ball.hit(block, hitSizeX ,hitSizeY):
                hit+=1
                block.y=0
                block.x=0
                self.score += 1
        if hit>0:
            self.ball.vx *=-1
            self.ball.vy *=-1