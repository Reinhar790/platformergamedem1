import os

SCREEN_WIDTH=1000
SCREEN_HEIGHT=500
SCREEN_TITLE='Arcade tiled map implementation'

PLAYER_SPEED=4
PLAYER_JUMP=12
GRAVITY=0.9
PLAYER_MAX_LIFE=5

MAP_NAME_STAGE_1=os.path.join(os.path.dirname(__file__),'map.tmj')
MAP_NAME_STAGE_2=os.path.join(os.path.dirname(__file__),'map2.tmj')

class GameState:
    START = 0
    PLAYING = 1
    GAME_OVER = 2
    FINISH = 3