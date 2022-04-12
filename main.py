from Game.ChessMain import Game
from Game.DumbChessEngine import DumbChessEngine
from Game.DailyPuzzle import DailyPuzzle

mode = int(input("Type 0 for new game or 1 for chess.com daily puzzle \n"))

if mode == 0:
    Game(DumbChessEngine()).play()
else:
    Game(DumbChessEngine(), DailyPuzzle()).play()
