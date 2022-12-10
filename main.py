from Engines.DeepChessEngine import DeepChessEngine
from Game.ChessMain import Game
from Engines.DumbChessEngine import DumbChessEngine
from Engines.MiniMaxClassical import MiniMaxClassical
from Engines.DeepChessEngine import DeepChessEngine
from Engines.DeepChessComputer import DeepChessComputer
from Game.DailyPuzzle import DailyPuzzle
from Game.EngineVsEngine import EngineVsEngine

from Engines.testmodel import TestModel

import chess as ch
import random as rd
import numpy as np

import chess as ch

if __name__ == '__main__':

    # mode = input("Type 'n' for new game, 'p' for a random chess.com daily puzzle or 'e' for Engine vs Engine \n")

    # if mode == 'p':
    #     Game(DumbChessEngine(), DailyPuzzle()).play()
    # elif mode == 'e':
    #     color = input("Who play with white 'd' or 'm'\n")
    #     if color == 'm':
    #         EngineVsEngine(DumbChessEngine(), MiniMaxClassical()).play()
    #     else:
    #         EngineVsEngine(MiniMaxClassical(), DumbChessEngine()).play()
    # else:
    #     color = input("Type 'b' for black or 'w' for white\n")
    #     engine = input("Type 'd' for dumb or 'm' for minimax\n")
    #     if color == 'b' and engine == 'd':
    #         Game(DumbChessEngine(), ch.BLACK).play()
    #     elif color == 'w' and engine == 'd':
    #         Game(DumbChessEngine(), ch.WHITE).play()
    #     elif color == 'b' and engine == 'm':
    #         Game(MiniMaxClassical(), ch.BLACK).play()
    #     else:
    #         Game(MiniMaxClassical(), ch.WHITE).play()

    Game(DeepChessEngine(),  ch.WHITE).play()
    # EngineVsEngine(DeepChessComputer(), DeepChessEngine()).play()
    # EngineVsEngine(DeepChessEngine(), DeepChessComputer()).play()

    # EngineVsEngine(MiniMaxClassical(), DeepChessComputer()).play()
    # EngineVsEngine(DeepChessComputer(), MiniMaxClassical()).play()


    # board1 = ch.Board()
    # board1.push_san("b1a3")

    # board2 = ch.Board()
    # board2.push_san("e2e4")

    # testModel = TestModel()

    # print(board1)
    # print(board2)

    # result = testModel.compare_positions(board1, board2)

    # print(result)

    # arr = np.arange(100)
    # print(arr)
    # games_wins_crop = arr[np.random.choice(len(arr), size=50, replace=False)]
    # print(games_wins_crop)