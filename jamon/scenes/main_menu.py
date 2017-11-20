from jamon.game.game import Scene, GameObject
from jamon.game.components.graphics import *
from jamon.scenes.scene_util import *
from kivy.core.window import Window

from jamon.game.controller import Keyboard

scene = Scene('main_menu', start=True)

BUTTON_WIDTH = Window.width / 3.0
BUTTON_HEIGHT = Window.height / 4.0
PERCENT_WINDOW_BUTTONS = .666


header = GameObject()
# TODO add Jam On Label

host_game_rect = RectSprite((BUTTON_WIDTH, BUTTON_HEIGHT), (0.2, 0.3, 0.7))
host_game_rect.center = (Window.width / 3.5, Window.height / 3.5)

host_game_button = Button(host_game_rect)
# TODO add callback for the button


join_game_rect = RectSprite((BUTTON_WIDTH, BUTTON_HEIGHT), (0.7, 0.2, 0.3))
join_game_rect.center = (2.7 * Window.width / 3.5, Window.height / 3.5)

join_game_button = Button(join_game_rect)
# TODO add callback for the button





# circle = GameObject()
# sprite = CircleSprite(100, (1, 0, 0))
# sprite.center = (0, 0)
# circle.add_graphic(sprite)

# circle2 = GameObject()
# circle2.scale = 0.5
# sprite = CircleSprite(100, (0, 0, 1))
# sprite.center = (0, 0)
# circle2.add_graphic(sprite)

# circle3 = GameObject()
# circle3.scale = 0.5
# sprite = CircleSprite(100, (0, 1, 0))
# sprite.center = (0, 0)
# circle3.add_graphic(sprite)

# circle.add_game_object(circle2)
# circle2.add_game_object(circle3)


# circle.position = (50, 50)
# button.sprite.center = (0, 0)
# scene.add_game_object(circle)
scene.add_game_object(host_game_button)
scene.add_game_object(join_game_button)
# scene.add_game_object(Keyboard())
