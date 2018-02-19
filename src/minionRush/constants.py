'''
Created on 2-Nov-2017

@author: Kavya Reddy
@author: Priyanka Gadde
'''
# Colors
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
LIGHTGREEN = (0, 255, 192)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 96, 255)

# Settings
FONT_NAME = 'arial'
BGCOLOR = LIGHTBLUE
SPRITESHEET = 'spritesheet_jumper.png'
HS_FILE = "highscore.txt"


# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 600

BOOST_POWER = 30
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2

# Platforms
PLATFORM_LIST = [(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
                 (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT * 3 / 4, 100, 20),
                 (125, SCREEN_HEIGHT - 250, 100, 20),
                 (300, 250, 100, 20),
                 (180, 150, 50, 20)]


# Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.15
PLAYER_GRAV = 0.8
PLAYER_JUMP = 22
