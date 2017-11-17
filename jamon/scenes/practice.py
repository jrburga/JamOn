from jamon.game.game import Scene, GameObject
from jamon.game.track import Gem

scene = Scene('practice')

gem = Gem((1, 0, 0))

scene.add_game_object(gem)