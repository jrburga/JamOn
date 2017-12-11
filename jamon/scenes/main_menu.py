from jamon.game.game import Scene, GameObject
from jamon.game.widgets import *
from jamon.game.components.graphics import *
from jamon.game.text import TextObject
from jamon.game.window import Window
from kivy.graphics import Color
import time

class MainMenu(Scene):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        print kwargs
        self.start_time = time.time()

    def on_load(self):
        self.make_buttons()
        self.make_header()

    def make_header(self):
        header_str = "[anchor=left][size=200][b][i]Jam On![/i][/b][/size][anchor=right]"
        header = TextObject(header_str, markup=True, color=(0,0,0), halign='center', 
                            valign='bottom', size=(Window.width * 0.8, Window.height/4.0))
        header.position = (Window.width * 0.1, 0.75 * Window.height)
        self.add_game_object(header)

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

        host_game_button = Button(pos=(left_x, y), background_color=BLUE + (1.0,),# background_down=DARK_BLUE + (1.0,),
                                  size=(BUTTON_WIDTH, BUTTON_HEIGHT), background_normal='',
                                  text="[size=150]Host[/size]", markup=True)
        host_game_button.bind(host_game_cb)

        def join_game_cb(go):
            go.trigger_event('on_server_request', server_type='join_game')
            go.trigger_event('on_scene_change', scene_name='join_game')

        join_game_button = Button(pos=(right_x, y), 
                                  size=(BUTTON_WIDTH, BUTTON_HEIGHT), background_color=GREEN + (1.0,),
                                  text="[size=150]Join[/size]",  background_normal='', # background_down=DARK_GREEN + (1.0,),
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

    def on_update(self):
        
        pass

def build_scene(**kwargs):
    return MainMenu(**kwargs)

