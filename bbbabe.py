import arcade,sys
from modelsBBBABE import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

k=open('min.txt','a')
k.close()

readfileBeforeKeepScore = open('min.txt', 'r')
minSC = readfileBeforeKeepScore.readline()

if minSC == "":
    writefile = open('min.txt','w')
    writefile.write("100")
    writefile.close()

readfileBeforeKeepScore.close()

readfile = open('min.txt', 'r')
min = readfile.readline()

class ModelSprite(arcade.Sprite):
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


    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
        self.x = self.model.x
        self.y = self.model.y
        self.hp = self.model.hp
        self.image = self.changeImageByHp() 
        

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle
            self.hp = self.model.hp
            self.image =self.changeImageByHp() 


    def draw(self):
        self.sync_with_model()
        super().draw()


class SpaceGameWindow(arcade.Window):
    
    def __init__(self,width,height):
        super().__init__(width,height)
        arcade.set_background_color(arcade.color.WHITE)
        self.world = World(width, height,self)

        self.ball_sprite = []
        self.ball_sprite.append(ModelSprite('images/ball.png',model=self.world.balls[0]))

        self.arrow_sprite = ModelSprite('images/arrow1.png',model=self.world.arrow)
        self.block_sprite = []
        for block in self.world.blocks:
            self.block_sprite.append(ModelSprite(block.image,model=block))
            

    def on_draw(self):
        arcade.start_render()

        for block in self.block_sprite:
                block.draw()
                block = ModelSprite(block.image,model=block)
                block.draw()
            
        self.arrow_sprite.draw()

        for ball in self.ball_sprite:
            ball.draw()

        arcade.draw_text("SCORE: "+str(self.world.score),
                         self.width - 120, self.height - 30,
                         arcade.color.AZURE, 20)

        arcade.draw_text("MIN: "+ min ,
                         self.width - 240, self.height - 30,
                         arcade.color.BITTERSWEET, 20)
        
        arcade.draw_text("Ball: "+str(self.world.noOfBall),
                         0, self.height - 30,
                         arcade.color.AZURE, 20)

        if self.world.blockleft <= 0:
            if self.world.score <= int(min):
                writefile = open('min.txt','w')
                writefile.write( str(self.world.score) )
                writefile.close()
                readfile.close()
            sys.exit()


    def update(self,delta):
        self.world.update(delta)
    def on_key_press(self,key,key_modifiers):
        self.world.on_key_press(key,key_modifiers)
    def on_key_release(self,key,key_modifiers):
        self.world.on_key_release(key,key_modifiers)
    def check_for_collision(self,other):
        self.world.ball.check_for_collision(other)
    def insert_ball(self, x):
        self.ball_sprite.append(ModelSprite('images/ball.png',model=x))

if __name__ == '__main__':
    windows = SpaceGameWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    arcade.run()