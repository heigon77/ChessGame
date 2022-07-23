import chess as ch
import random as rd


class MiniMaxClassical:

    def __init__(self):
        self.depth_lim = 1
        self.MAX = 1000
        self.MIN = -1000

    def choose_move(self, board: ch.Board()):
        """
        Choose any random move
        :param board:
        :return:
        """

        move = self.minimax(0, board, False, self.MIN, self.MAX)
        return move[1]

    # Returns optimal value for current player
    # (Initially called for root and maximizer)
    def minimax(self, depth, board, maximizingPlayer, alpha, beta):

        moves = list(board.legal_moves)

        # Terminating condition. i.e.
        # leaf node is reached
        if depth == self.depth_lim or self.game_finished(board):

            return self.evaluation(board), None

        if maximizingPlayer:

            best = self.MIN
            best_move = rd.choice(moves)

            # Recur for left and right children
            for i in moves:
                new_board = board.copy()
                new_board.push(i)
                val = self.minimax(depth + 1, new_board, False, alpha, beta)[0]

                if best > val:
                    best = val
                    best_move = i

                alpha = max(alpha, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best, best_move

        else:
            best = self.MAX
            best_move = rd.choice(moves)

            # Recur for left and
            # right children
            for i in moves:
                new_board = board.copy()
                new_board.push(i)
                val = self.minimax(depth + 1, new_board, True, alpha, beta)[0]

                if best < val:
                    best = val
                    best_move = i

                beta = min(beta, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best, best_move

    def evaluation(self, board):
        value = 0

        value += 200 * (self.count_pieces(board, ch.KING, ch.WHITE) - self.count_pieces(board, ch.KING, ch.BLACK))
        value += 9 * (self.count_pieces(board, ch.QUEEN, ch.WHITE) - self.count_pieces(board, ch.QUEEN, ch.BLACK))
        value += 5 * (self.count_pieces(board, ch.ROOK, ch.WHITE) - self.count_pieces(board, ch.ROOK, ch.BLACK))
        value += 3 * (self.count_pieces(board, ch.BISHOP, ch.WHITE) - self.count_pieces(board, ch.BISHOP, ch.BLACK))
        value += 3 * (self.count_pieces(board, ch.KNIGHT, ch.WHITE) - self.count_pieces(board, ch.KNIGHT, ch.BLACK))
        value += 1 * (self.count_pieces(board, ch.PAWN, ch.WHITE) - self.count_pieces(board, ch.PAWN, ch.BLACK))

        return value

    def count_pieces(self, board, piece, color):
        pieces = board.pieces(piece_type=piece, color=color).tolist().count(True)

        return pieces

    def game_finished(self, board):
        """
        Verifies is the game ended
        :return:
        """

        if board.is_checkmate():
            return True

        elif board.is_stalemate():
            return True

        elif board.is_insufficient_material():
            return True

        elif board.can_claim_threefold_repetition():
            return True

        return False
