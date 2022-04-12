from Game.ChessMain import Game
from Game.DumbChessEngine import DumbChessEngine
from Game.DailyPuzzle import DailyPuzzle
import chess as ch

if __name__ == '__main__':

    mode = input("Type n for new game or p for chess.com daily puzzle \n")

    if mode == 'p':
        Game(DumbChessEngine(), DailyPuzzle()).play()
    else:
        color = input("Type b for black or w for white\n")
        if color == 'b':
            Game(DumbChessEngine(), ch.BLACK).play()
        else:
            Game(DumbChessEngine(), ch.WHITE).play()
