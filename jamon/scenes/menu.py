from jamon.game.game import Scene, GameObject
from jamon.game.widgets import *
from jamon.game.components.graphics import *
from jamon.game.player import Player

scene = Scene('menu')

# scene.add_event_listener('on_key_down', print_event)
textinput = TextBox(text='Hello world', 
					  multiline=False)
button = Button(text='Hello world')

# textinput.position = (100, 100)
button.position = (100, 100)

scene.add(textinput)
scene.add(button)
