from BoardGames.CantStop import Game, Components, Player
import importlib
importlib.reload(Game)
importlib.reload(Components)
importlib.reload(Player)

game = Game.Game()