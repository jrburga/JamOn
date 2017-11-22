from jamon.game.game import Scene, GameObject
from jamon.game.session import Session

scene = Scene('practice', start=True)

scene.add_game_object(Session())
