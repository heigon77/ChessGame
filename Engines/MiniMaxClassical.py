import chess as ch
import random as rd


class MiniMaxClassical:

    def __init__(self):
        self.depth_lim = 3
        self.MAX = 1000
        self.MIN = -1000

    def choose_move(self, board: ch.Board(), color):
        """
        Choose any random move
        :param color:
        :param board:
        :return:
        """
        if color == ch.WHITE:
            max_player = True
        else:
            max_player = False

        move = self.minimax(0, board, max_player, self.MIN, self.MAX)
        nboard = board.copy()
        nboard.push(move[1])

        print("Escolhido: ", self.evaluation(board), move[1])

        return move[1]

    # Returns optimal value for current player
    # (Initially called for root and maximizer)
    def minimax(self, depth, board, maximizingPlayer, alpha, beta):

        moves = list(board.legal_moves)

        # Terminating condition. i.e.
        # leaf node is reached
        print(self.evaluation(board), maximizingPlayer, depth)
        if depth == self.depth_lim or len(moves) == 0:
            return self.evaluation(board), None

        if maximizingPlayer:

            best = self.MIN
            best_move = rd.choice(moves)

            # Recur for left and right children
            for i in moves:
                new_board = board.copy()
                new_board.push(i)
                val = self.minimax(depth + 1, new_board, False, alpha, beta)[0]

                if val > best:
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

                if val < best:
                    best = val
                    best_move = i

                beta = min(beta, best)

                # Alpha Beta Pruning
                if beta <= alpha:
                    break

            return best, best_move

    def evaluation(self, board):
        value = 0

        value += self.game_finished_value(board)
        value += 9 * (self.count_pieces(board, ch.QUEEN, ch.WHITE) - self.count_pieces(board, ch.QUEEN, ch.BLACK))
        value += 5 * (self.count_pieces(board, ch.ROOK, ch.WHITE) - self.count_pieces(board, ch.ROOK, ch.BLACK))
        value += 3 * (self.count_pieces(board, ch.BISHOP, ch.WHITE) - self.count_pieces(board, ch.BISHOP, ch.BLACK))
        value += 3 * (self.count_pieces(board, ch.KNIGHT, ch.WHITE) - self.count_pieces(board, ch.KNIGHT, ch.BLACK))
        value += 1 * (self.count_pieces(board, ch.PAWN, ch.WHITE) - self.count_pieces(board, ch.PAWN, ch.BLACK))

        # 27 28 35 36
        white_attk = 0
        black_attk = 0
        for i in range(64):
            if i == 27 or 28 or 35 or 36:
                if board.is_attacked_by(ch.WHITE, i):
                    white_attk += 0.1
                if board.is_attacked_by(ch.BLACK, i):
                    black_attk += 0.1
            else:
                if board.is_attacked_by(ch.WHITE, i):
                    white_attk += 0.05
                if board.is_attacked_by(ch.BLACK, i):
                    black_attk += 0.05



        value += white_attk - black_attk

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

    def game_finished_value(self, board):
        """
        Verifies is the game ended
        :return:
        """

        if board.is_checkmate():
            if board.outcome().winner == ch.WHITE:
                return 200
            else:
                return -200

        elif board.is_stalemate():
            return 0

        elif board.is_insufficient_material():
            return 0

        elif board.can_claim_threefold_repetition():
            return 0

        return 0
