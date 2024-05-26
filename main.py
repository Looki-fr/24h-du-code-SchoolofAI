from tools.Game import Game
import os
current_path=os.path.dirname(__file__)

game=Game(current_path)
while not game.finish:
    game.update()
