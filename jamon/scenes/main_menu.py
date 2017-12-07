from jamon.game.game import Scene, GameObject
from jamon.game.widgets import *
from jamon.game.components.graphics import *
from jamon.game.window import Window

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

        def host_game_cb(go):
            go.trigger_event('on_server_request', server_type='host_game')
            go.trigger_event('on_scene_change', scene_name='waiting_room', is_host=True)

        host_game_button = Button(pos=(left_x_center, top_y_center), 
                                  size=(BUTTON_WIDTH, BUTTON_HEIGHT), 
                                  text="Host Game")
        host_game_button.bind(host_game_cb)

        def join_game_cb(go):
            go.trigger_event('on_server_request', server_type='join_game')
            go.trigger_event('on_scene_change', scene_name='join_game')

        join_game_button = Button(pos=(right_x_center, top_y_center), 
                                  size=(BUTTON_WIDTH, BUTTON_HEIGHT), 
                                  text="Join Game")
        join_game_button.bind(join_game_cb)

        def change_username_cb(go):
            go.trigger_event('on_scene_change', scene_name='change_username')

        change_username_button = Button(pos=(left_x_center, bottom_y_center), 
                                        size=(BUTTON_WIDTH, BUTTON_HEIGHT), 
                                        text="Change Username")
        change_username_button.bind(change_username_cb)

        self.add_game_object(host_game_button)
        self.add_game_object(join_game_button)
        self.add_game_object(change_username_button)

def build_scene(**kwargs):
    return MainMenu(**kwargs)

