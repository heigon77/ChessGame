from Game.ChessMain import Game
from Game.DumbChessEngine import DumbChessEngine
from Game.DailyPuzzle import DailyPuzzle
from Game.EngineVsEngine import EngineVsEngine

import chess as ch

if __name__ == '__main__':

    mode = input("Type 'n' for new game, 'p' for a random chess.com daily puzzle or 'e' for Engine vs Engine \n")

    if mode == 'p':
        Game(DumbChessEngine(), DailyPuzzle()).play()
    elif mode == 'e':
        EngineVsEngine(DumbChessEngine(), DumbChessEngine()).play()
    else:
        color = input("Type 'b' for black or 'w' for white\n")
        if color == 'b':
            Game(DumbChessEngine(), ch.BLACK).play()
        else:
            Game(DumbChessEngine(), ch.WHITE).play()
