import chess as ch
import random as rd

class DumbChessEngine:

    def __init__(self):
        pass

    def choose_move(self, board: ch.Board()):
        """
        Choose any random move
        :param board:
        :return:
        """
        moves = list(board.legal_moves)
        return rd.choice(moves)
