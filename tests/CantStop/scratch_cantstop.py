from BoardGames.CantStop import Game, Components, Player
import importlib
import pickle
importlib.reload(Game)
importlib.reload(Components)
importlib.reload(Player)

state = pickle.load(open('random states/rand_state04.p', 'rb'))
game = Game.Game(random_state=state)

# game = Game.Game()
