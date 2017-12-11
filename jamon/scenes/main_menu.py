from jamon.game.game import Scene, GameObject
from jamon.game.widgets import *
from jamon.game.components.graphics import *
from jamon.game.window import Window
from kivy.graphics import Color

class MainMenu(Scene):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        print kwargs

    def on_load(self):
        self.make_buttons()

    def make_buttons(self):
        BUTTON_WIDTH = Window.width * 0.45
        BUTTON_HEIGHT = Window.height * 0.6
        PERCENT_WINDOW_BUTTONS = .70

        AREA_WIDTH = Window.width
        AREA_HEIGHT = Window.height * PERCENT_WINDOW_BUTTONS

        # Centers of the 2x2 Buttons:
        left_x = AREA_WIDTH * 1./3 - 4.0 * BUTTON_WIDTH / 6.0
        right_x = AREA_WIDTH * 2./3 - 2.0 * BUTTON_WIDTH / 6.0

        y = AREA_HEIGHT * 1./2.0 - BUTTON_HEIGHT / 2.0
        # top_y_center = AREA_HEIGHT * 1./2.0

        def host_game_cb(go):
            go.trigger_event('on_server_request', server_type='host_game')
            go.trigger_event('on_scene_change', scene_name='waiting_room', is_host=True)

        host_game_button = Button(pos=(left_x, y), background_color=BLUE + (1.0,),
                                  size=(BUTTON_WIDTH, BUTTON_HEIGHT), background_normal='',
                                  text="[size=150]Host[/size]", markup=True)
        host_game_button.bind(host_game_cb)

        def join_game_cb(go):
            go.trigger_event('on_server_request', server_type='join_game')
            go.trigger_event('on_scene_change', scene_name='join_game')

        join_game_button = Button(pos=(right_x, y), 
                                  size=(BUTTON_WIDTH, BUTTON_HEIGHT), background_color=GREEN + (1.0,),
                                  text="[size=150]Join[/size]",  background_normal='', 
                                  markup=True)
        join_game_button.bind(join_game_cb)

        # def change_username_cb(go):
        #     go.trigger_event('on_scene_change', scene_name='change_username')

        # change_username_button = Button(pos=(left_x_center, bottom_y_center), 
        #                                 size=(BUTTON_WIDTH, BUTTON_HEIGHT), 
        #                                 text="Change Username")
        # change_username_button.bind(change_username_cb)

        self.add_game_object(host_game_button)
        self.add_game_object(join_game_button)
        # self.add_game_object(change_username_button)

def build_scene(**kwargs):
    return MainMenu(**kwargs)

