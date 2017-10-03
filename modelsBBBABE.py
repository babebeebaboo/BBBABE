import arcade.key
import arcade
from random import randint
import math


class Model:
    def __init__(self,world,x,y,vx,vy,angle=0,hp=0):
        self.x = x
        self.y = y
        #self.center_x = x
        #self.center_y = y
        self.vx = vx
        self.vy = vy
        self.world = world
        self.angle = angle
        self.hp = hp

    def collision(self,other):
        '''
        down = arcade.Sprite('images/blockdown.png')
        up = arcade.Sprite('images/blockup.png')
        left = arcade.Sprite('images/blockleft.png')
        right = arcade.Sprite('images/blockright.png')

        ball = arcade.Sprite('images/ball.png')
        '''
        '''
        print("Down ",end='')
        print(down.points)
        '''
        '''
        print("Up ",end='')
        print(up.points)
        print("Left ",end='')
        print(left.points)
        print("Right ",end='')
        print(right.points)
        '''
        '''
        down.center_x = other.x
        down.center_y = other.y - 15/2
        '''
        down1 = ( (other.x - 30, other.y - 15),(other.x + 30, other.y - 15) , (other.x + 30, other.y-14), (other.x - 30, other.y-14))
        up1 = ( (other.x - 30, other.y + 15),(other.x + 30, other.y + 15) , (other.x + 30, other.y+16), (other.x - 30, other.y+16))
        left1 = ( (other.x - 30, other.y - 15),(other.x - 29, other.y -15) , (other.x - 29, other.y+15), (other.x - 30, other.y+15))
        right1 = ( (other.x + 29, other.y -15),(other.x + 30, other.y - 15), (other.x + 30, other.y+15), (other.x + 29, other.y+15))
        ball = ( (self.x - 10,self.y-10) , (self.x + 10,self.y- 10) , (self.x + 10,self.y+ 10) , (self.x - 10,self.y + 10))
        '''
        print("Down1 ",end='')
        print(down.points)
        up.center_x = other.x
        up.center_y = other.y + 15/2

        left.center_x = other.x - 15
        left.center_y = other.y 

        right.center_x = other.x + 15
        right.center_y = other.y

        ball.center_x = self.x
        ball.center_y = self.y
        '''
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
        '''
        print("Delta = ",end='')
        print(delta)
        '''
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
            
            ###if ( math.atan2(self.ball.x-block.x , self.ball.y-block.y) >= math.atan2( 0 - 30 , 0-15) and math.atan2(self.ball.x-block.x , self.ball.y-block.y) <= math.atan2( 60 - 30 , 0-15) ) or( math.atan2(self.ball.x-block.x , self.ball.y-block.y) >= math.atan2(0-blockX , 30-blockY) and math.atan2(self.ball.x-block.x , self.ball.y-block.y)<= math.atan2(60-blockX , 30-blockY) ):
            #if self.ball.ballHitBlock(block) :

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
                        
                '''
                if abs(self.ball.vx) > abs(self.ball.vy):
                    changeX += 1
                elif abs(self.ball.vy) > abs(self.ball.vx) :
                    changeY += 1 
                else :
                    changeX += 1
                    changeY += 1 
                '''

                
                ''' 
                    ต้องหาจุดของวงกลมที่เข้าใกล้ x y ของสี่เหลี่ยมที่มากที่สุด แล้วจะใช้เป็น x y ในการหา arctan

                    ยังแก้ปัญหาถ้ายิงชึ้นตรงๆตรงระหว่างลูกแล้วลูกควรลงแต่ลงไม่ได้ มันเปลี่ยนด้าน L แต่ความจริงควรเปลี่ยนด้าน K
                '''
                '''
                  M
                |---|
              N |   | L
                |---|
                  K
                '''


                '''
                min=10000
                for i in range(0,90+1):
                        x = math.cos(math.degrees(i)) * 15
                        y = math.sin(math.degrees(90-i)) * 15
                        r = ( (block.x - x)**2 + (block.y -y )**2 ) ** 0.5
                        if r < min :
                            r = min
                            ansX = x
                            ansY = y
                for i in range(-90,0+1):
                        x = math.cos(math.degrees(i)) * 15
                        y = math.sin(math.degrees(90-i)) * 15
                        r = ( (block.x - x)**2 + (block.y -y )**2 ) ** 0.5
                        if r < min :
                            r = min
                            ansX = x
                            ansY = y
                for i in range(0,90+1):
                        x = math.cos(math.degrees(90-i)) * 15
                        y = math.sin(math.degrees(i)) * 15
                        r = ( (block.x - x)**2 + (block.y -y )**2 ) ** 0.5
                        if r < min :
                            r = min
                            ansX = x
                            ansY = y
                for i in range(-90,0+1):
                        x = math.cos(math.degrees(90-i)) * 15
                        y = math.sin(math.degrees(i)) * 15
                        r = ( (block.x - x)**2 + (block.y -y )**2 ) ** 0.5
                        if r < min :
                            r = min
                            ansX = x
                            ansY = y

                tan = math.atan2(abs(block.y - ansY ) , abs(block.x - ansX) )
                # N
                if tan > -2.0344439357957027 and tan < -1.1071487177940904  :
                    changeX += 1
                    #self.ball.x = block.x - 30 
                #L
                elif tan > 1.1071487177940904 and tan < 2.0344439357957027 :
                    changeX += 1
                    #self.ball.x = block.x + 30 
                #M
                elif tan > -1.1071487177940904 and tan < 1.1071487177940904 :
                    changeY += 1
                    #self.ball.y = block.y - 15
                #K
                elif tan >-3.0750244898139694 and tan< -2.0344439357957027 : 
                    changeY += 1
                    #self.ball.y = block.y + 15
                elif tan > 2.0481417091685685 and tan < 3.141592653589793 :
                    changeY += 1
                    #self.ball.y = block.y + 15
                # EDGE 
                elif abs(tan) == 2.0344439357957027 or abs(tan) == 1.1071487177940904:
                    changeX += 1
                    changeY += 1
                '''


                '''
                if tan < 0.5 :
                    changeX += 1
                    ###self.ball.x = min( block.y - self.ball.y)
                
                '''
                
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
            print ("VX = "+ str(self.ball.vx) + " VY = "+str(self.ball.vy) )
            print()
            '''
            self.ball.vx *=-1
            self.ball.vy *=-1
            '''