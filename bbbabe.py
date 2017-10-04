import arcade
from modelsBBBABE import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

class ModelSprite(arcade.Sprite):
    def changeImageByHp(self):
        image = ""
        if self.hp == 0 :
            image = "images/blockwhite.png"
        if self.hp == 1 :
            image = "images/block1.png"
        if self.hp == 2 :
            image = "images/block2.png"
        if self.hp == 3 :
            image = "images/block3.png"
        if self.hp == 4 :
            image = "images/block4.png"
        if self.hp == 5 :
            image = "images/block5.png"
        if self.hp == 6 :
            image = "images/block6.png"
        if self.hp == 7 :
            image = "images/block7.png"
        if self.hp == 8 :
            image = "images/block8.png"
        if self.hp == 9 :
            image = "images/block+.png"

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
            self.image = self.changeImageByHp()

    def draw(self):
        self.sync_with_model()
        super().draw()

class SpaceGameWindow(arcade.Window):
    def __init__(self,width,height):
        super().__init__(width,height)
        arcade.set_background_color(arcade.color.WHITE)
        self.world = World(width, height)
        self.ball_sprite = ModelSprite('images/ball.png',model=self.world.ball)
        self.arrow_sprite = ModelSprite('images/arrow1.png',model=self.world.arrow)
        self.block_sprite = []
        self.oldscore = []
        self.oldscore = self.world.blockshp
        
        for block in self.world.blocks:
            self.block_sprite.append(ModelSprite(block.image,model=block))
            
    def on_draw(self):
        arcade.start_render()
        #if self.oldscore == self.world.blockshp:
        for block in self.block_sprite:
                block.draw()
                block = ModelSprite(block.image,model=block)
                block.draw()

        self.arrow_sprite.draw()
        self.ball_sprite.draw()
        arcade.draw_text(str(self.world.blockleft),
                         self.width - 60, self.height - 60,
                         arcade.color.BLUE, 20)
        
        arcade.draw_text(str(self.world.score),
                         self.width - 60, self.height - 30,
                         arcade.color.BLUE, 20)

    def update(self,delta):
        self.world.update(delta)
    def on_key_press(self,key,key_modifiers):
        self.world.on_key_press(key,key_modifiers)
    def on_key_release(self,key,key_modifiers):
        self.world.on_key_release(key,key_modifiers)

    def check_for_collision(self,other):
        self.world.ball.check_for_collision(other)

if __name__ == '__main__':
    windows = SpaceGameWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    arcade.run()