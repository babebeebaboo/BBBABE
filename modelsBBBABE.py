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
    def hit(self,other,hit_sizeX,hit_sizeY):
        return (abs(self.x - other.x) <= hit_sizeX) and (abs(self.y - other.y) <= hit_sizeY)
'''
        collision_radius_sum = self. + sprite2.collision_radius

        diff_x = sprite1.position[0] - sprite2.position[0]
        diff_x2 = diff_x * diff_x

        if diff_x2 > collision_radius_sum * collision_radius_sum:
            return False

        diff_y = sprite1.position[1] - sprite2.position[1]
        diff_y2 = diff_y * diff_y
        if diff_y2 > collision_radius_sum * collision_radius_sum:
            return False

        distance = diff_x2 + diff_y2
        if distance > collision_radius_sum * collision_radius_sum:
            return False

        return are_polygons_intersecting(sprite1.points, sprite2.points)
'''

def GenerateBlock():
    return [[randint(0,3) for x in range(0,8)] for y in range(17)]

class Block(Model):
    def __init__(self,world,x,y,hp,vx=0,vy=0,angle=0):
        super().__init__(world,x,y,vx,vy,angle,hp)
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
    def update(self,delta):
        pass

class Arrow(Model):
    def __init__(self,world,x,y,vx,vy,angle,move=1):
        super().__init__(world,x,y,vx,vy,angle)
        self.move = move
    def update(self,delta):
        
        self.angle += self.move 
        if self.angle <= 0+5 or self.angle >= 180-5: 
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
            print ( str(self.ball.vx) + " "+str(self.ball.vy) )
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
        for block in self.blocks:
            block.update(delta)
            
            hitSizeX = 30 + self.ball.radius
            hitSizeY = 15 + self.ball.radius
            ###if ( math.atan2(self.ball.x-block.x , self.ball.y-block.y) >= math.atan2( 0 - 30 , 0-15) and math.atan2(self.ball.x-block.x , self.ball.y-block.y) <= math.atan2( 60 - 30 , 0-15) ) or( math.atan2(self.ball.x-block.x , self.ball.y-block.y) >= math.atan2(0-blockX , 30-blockY) and math.atan2(self.ball.x-block.x , self.ball.y-block.y)<= math.atan2(60-blockX , 30-blockY) ):
            if self.ball.hit(block,hitSizeX,hitSizeY) :
                if math.atan2(abs(block.y - self.ball.y) , abs(block.x - self.ball.x) ) >= 0.5:
                    changeY += 1

                if math.atan2(abs(block.y - self.ball.y) , abs(block.x - self.ball.x) ) < 0.5 :
                    changeX += 1
                    ###self.ball.x = min( block.y - self.ball.y)

                print ( "X "+"Ball: "+str(self.ball.x) + " "+"Block: "+str(block.x) +" "+"Range: "+ str( abs(block.x - self.ball.x) ) )
                print("Y "+"Ball: "+str(self.ball.y) + " "+"Block: "+str(block.y)+" "+"Range: "+ str( abs(block.y - self.ball.y) ) )
                print("Atan = " + str( math.atan2(abs(block.y - self.ball.y) , abs(block.x - self.ball.x) ) ))
                hit+=1
                block.hp -= 1
                if block.hp <=0:
                    block.y=-100
                    block.x=-100
                    self.breakBlock += 1
        if hit>0:
            '''
            if (self.x < self.radius) or (self.x > self.world.width-self.radius):
                self.vx = - self.vx
        
            if (self.y < self.radius) or (self.y > self.world.height-self.radius):
                self.vy = - self.vy
            '''
            if changeX >0:
                self.ball.vx *= -1
                
            if changeY >0:
                self.ball.vy *= -1
            print ( str(self.ball.vx) + " "+str(self.ball.vy) )
            print()
            '''
            self.ball.vx *=-1
            self.ball.vy *=-1
            '''