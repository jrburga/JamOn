from jamon.game.game import Scene, GameObject
from jamon.game.widgets import *
from jamon.game.components.graphics import *
from kivy.core.window import Window

from jamon.game.controller import Keyboard

class MainMenu(Scene):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        print kwargs
        self.make_buttons()

    def make_buttons(self):
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

        def button_actions(button_str):
            def callback_fn(go):
                if button_str in ['join_game', 'host_game']:
                    go.trigger_event('on_server_request', server_type=button_str)
                go.trigger_event('on_scene_change', scene_name=button_str)
            return callback_fn

        host_game_button = Button(pos=(left_x_center, top_y_center), 
                                  size=(BUTTON_WIDTH, BUTTON_HEIGHT), 
                                  text="Host Game")
        host_game_button.bind(button_actions('host_game'))

        join_game_button = Button(pos=(right_x_center, top_y_center), 
                                  size=(BUTTON_WIDTH, BUTTON_HEIGHT), 
                                  text="Join Game")
        join_game_button.bind(button_actions('join_game'))

        change_username_button = Button(pos=(left_x_center, bottom_y_center), 
                                        size=(BUTTON_WIDTH, BUTTON_HEIGHT), 
                                        text="Change Username")
        change_username_button.bind(button_actions('change_username'))

        self.add_game_object(host_game_button)
        self.add_game_object(join_game_button)
        self.add_game_object(change_username_button)

def build_scene(**kwargs):
    return MainMenu(**kwargs)

