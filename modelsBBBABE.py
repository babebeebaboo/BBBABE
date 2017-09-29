import arcade.key

class Model:
    def __init__(self,world,x,y,vx,vy,angle=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.world = world
        self.angle = angle

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
    def __init__(self,world,x,y,vx,vy,size):
        super().__init__(world,x,y,vx,vy)
        self.size = size
        self.radius = size/2

    def shoot(self,angle):
        maxspeed = 15
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

class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.ball = Ball(self,300,20,0,0,30)
        self.arrow = Arrow(self,300,20,0,0,179,2)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ball.shoot(self.arrow.angle)
            
    def update(self,delta):
        self.ball.update(delta)
        self.arrow.update(delta)