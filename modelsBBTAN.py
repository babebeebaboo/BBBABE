class Ball():
    def __init__ (self,world,x,y,vx,vy):
        self.world = world
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def random_direction(self):
        self.vx = 5*random()
    def update(self,delta):
        if (self.x < 0) or (self.x > self.world.width):
            self.vx = - self.vx
        
        if (self.y < 0) or (self.y > self.world.height):
            self.vy = - self.vy
        self.x += self.vx
        self.y += self.vy


class World:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.ball = Ball(self,100,100,5,2)
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.switch_direction()
    def update(self,delta):
        self.ball.update(delta)
