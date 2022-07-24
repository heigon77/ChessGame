import chess as ch
import random as rd


class DumbChessEngine:

    def __init__(self):
        pass

    def choose_move(self, board: ch.Board(), color=None):
        """
        Choose any random move
        :param color:
        :param board:
        :return:
        """
        moves = list(board.legal_moves)
        return rd.choice(moves)
