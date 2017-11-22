from jamon.game.game import Scene, GameObject
from jamon.game.widgets import *
from jamon.game.components.graphics import *
from kivy.core.window import Window

from jamon.game.controller import Keyboard

scene = Scene('main_menu')

BUTTON_WIDTH = Window.width * 0.4
BUTTON_HEIGHT = Window.height / 3.5
PERCENT_WINDOW_BUTTONS = .70

AREA_WIDTH = Window.width
AREA_HEIGHT = Window.height * PERCENT_WINDOW_BUTTONS

# Centers of the 2x2 Buttons:
left_x_center = AREA_WIDTH * 1./3 - 4.0 * BUTTON_WIDTH / 6.0
right_x_center = AREA_WIDTH * 2./3 - 2.0 * BUTTON_WIDTH / 6.0

bottom_y_center = AREA_HEIGHT * 2./5 - 8./10 * BUTTON_HEIGHT
top_y_center = AREA_HEIGHT * 4./5 - 6./10 * BUTTON_HEIGHT

# TODO add callbacks, labels for the button, header label

# header = GameObject()

# host_game_rect = RectSprite((BUTTON_WIDTH, BUTTON_HEIGHT), (0.2, 0.3, 0.7)) # Add labels, label="Host Game"
host_game_button = Button()
host_game_button.position = (left_x_center, top_y_center)

# join_game_rect = RectSprite((BUTTON_WIDTH, BUTTON_HEIGHT), (0.7, 0.2, 0.3))
join_game_button = Button()
join_game_button.position = (right_x_center, top_y_center)

# change_username_rect = RectSprite((BUTTON_WIDTH, BUTTON_HEIGHT), (0.2, 0.7, 0.3))
change_username_button = Button()
change_username_button.position = (left_x_center, bottom_y_center)

scene.add_game_object(host_game_button)
scene.add_game_object(join_game_button)
scene.add_game_object(change_username_button)
