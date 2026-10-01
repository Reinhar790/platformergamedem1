from config import SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_TITLE, PLAYER_JUMP,PLAYER_MAX_LIFE
from config import PLAYER_SPEED,GRAVITY, MAP_NAME_STAGE_1,MAP_NAME_STAGE_2, GameState

import arcade
from startscreen import StartScreen

window=arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
start_view=StartScreen() 
window.show_view(start_view)
arcade.run()