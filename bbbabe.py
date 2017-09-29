import arcade
from modelsBBBABE import World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle

    def draw(self):
        self.sync_with_model()
        super().draw()

class SpaceGameWindow(arcade.Window):
    def __init__(self,width,height):
        super().__init__(width,height)
        arcade.set_background_color(arcade.color.BLACK)
        self.world = World(width, height)
        self.ball_sprite = ModelSprite('images/ball.png',model=self.world.ball)
        self.arrow_sprite = ModelSprite('images/arrow.png',model=self.world.arrow)

    def on_draw(self):
        arcade.start_render()
        self.arrow_sprite.draw()
        self.ball_sprite.draw()
    def update(self,delta):
        self.world.update(delta)
    def on_key_press(self,key,key_modifiers):
        self.world.on_key_press(key,key_modifiers)


if __name__ == '__main__':
    windows = SpaceGameWindow(SCREEN_WIDTH,SCREEN_HEIGHT)
    arcade.run()