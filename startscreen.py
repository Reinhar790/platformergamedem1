import arcade
from config import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, PLAYER_JUMP,PLAYER_MAX_LIFE
from config import PLAYER_SPEED,GRAVITY, MAP_NAME_STAGE_1,MAP_NAME_STAGE_2, GameState
from gameplay import Gameplay

class StartScreen(arcade.View):
    def __init__(self):
        super().__init__()

        bgm=arcade.load_sound("bgm.mp3")
        arcade.play_sound(bgm,volume=0.3,loop=True)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.icon=arcade.load_texture('start2.png')

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.icon,arcade.XYWH(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150, 180,180))
        arcade.draw_text("Press SPACE to start the game", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, arcade.color.WHITE, 28, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key==arcade.key.SPACE:
            view=Gameplay()
            view.setup()
            self.window.show_view(view)
            return