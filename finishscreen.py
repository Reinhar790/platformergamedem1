import arcade
from config import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, PLAYER_JUMP,PLAYER_MAX_LIFE
from config import PLAYER_SPEED,GRAVITY, MAP_NAME_STAGE_1,MAP_NAME_STAGE_2, GameState
from gameplay import Gameplay

class Gameoverscreen(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        self.iconfin=arcade.load_texture('dude2.png')
        arcade.set_background_color(arcade.color.AMAZON)
        return super().on_show_view()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.iconfin,arcade.XYWH(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 1000,500))
        arcade.draw_text("u win, space to go again", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE, 28, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key==arcade.key.SPACE:
            view=Gameplay()
            view.setup()
            self.window.show_view(view)
            return