import arcade
from modelsBBBABE import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
        self.x = self.model.x
        self.y = self.model.y
        self.hp = self.model.hp
        self.image = ""
        if self.hp == 0 :
            self.image = "images/blockwhite.png"
        if self.hp == 1 :
            self.image = "images/block1.png"
        if self.hp == 2 :
            self.image = "images/block2.png"
        if self.hp == 3 :
            self.image = "images/block3.png"
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            
            self.angle = self.model.angle

            self.hp = self.model.hp
            self.image = ""
            if self.hp == 0 :
                self.image = "images/blockwhite.png"
            if self.hp == 1 :
                self.image = "images/block1.png"
            if self.hp == 2 :
                self.image = "images/block2.png"
            if self.hp == 3 :
                self.image = "images/block3.png"

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
        for block in self.world.blocks:
            self.block_sprite.append(ModelSprite(block.image,model=block))
            
    def on_draw(self):
        arcade.start_render()
        
        for block in self.block_sprite:
            block.draw()
            block = ModelSprite(block.image,model=block)
            block.draw()

        self.arrow_sprite.draw()
        self.ball_sprite.draw()
        arcade.draw_text(str(self.world.noOfBlock - self.world.breakBlock),
                         self.width - 60, self.height - 60,
                         arcade.color.BLUE, 20)
        
        arcade.draw_text(str(self.world.score),
                         self.width - 60, self.height - 30,
                         arcade.color.BLUE, 20)

    def update(self,delta):
        self.world.update(delta)
    def on_key_press(self,key,key_modifiers):
        self.world.on_key_press(key,key_modifiers)

if __name__ == '__main__':
    windows = SpaceGameWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    arcade.run()