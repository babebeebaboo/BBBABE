BALLVX=5
BALLVY=10

class Ball():
    def __init__ (self,world,x,y,vx,vy):
        self.world = world
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = 30
        self.radius = 15
    def random_direction(self):
        self.vx = 5*random()
    def update(self,delta):
        if (self.x < self.radius) or (self.x > self.world.width-self.radius):
            self.vx = - self.vx
        
        if (self.y < self.radius) or (self.y > self.world.height-self.radius):
            self.vy = - self.vy
        self.x += self.vx
        self.y += self.vy


class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.ball = Ball(self,100,100,BALLVX,BALLVY)
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.switch_direction()
    def update(self,delta):
        self.ball.update(delta)
