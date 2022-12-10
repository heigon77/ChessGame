import chess as ch
import chess.pgn as pgn
from datetime import datetime


class EngineVsEngine:

    def __init__(self, chess_engine_black, chess_engine_white):
        self.chess_engine_black = chess_engine_black
        self.chess_engine_white = chess_engine_white
        self.board = None
        self.game = pgn.Game()
        self.first = True
        self.node = None

    def white_engine_choose_move(self):
        """
        The white engine update the board
        :return:
        """
        move = self.chess_engine_white.choose_move(self.board, ch.WHITE)
        if move:
            self.board.push(move)
            if self.first:
                self.first = False
                self.node = self.game.add_variation(move)
            else:
                self.node = self.node.add_variation(move)

        return

    def black_engine_choose_move(self):
        """
        The black engine update the board
        :return:
        """
        move = self.chess_engine_black.choose_move(self.board, ch.BLACK)
        if move:
            self.board.push(move)
            if self.first:
                self.first = False
                self.node = self.game.add_variation(move)
            else:
                self.node = self.node.add_variation(move)

        return

    def game_finished(self):
        """
        Verifies is the game ended
        :return:
        """
        f = open("Results.txt", "a")

        if self.board.is_checkmate():
            if self.board.outcome().winner == ch.WHITE:
                f.write("\nCheckmate - white win\n")
            else:
                f.write("\nCheckmate - black win\n")
            f.close()
            return True

        elif self.board.is_stalemate():
            f.write("\nStalemate\n")
            f.close()
            return True

        elif self.board.is_insufficient_material():
            f.write("\nDraw by insufficient material\n")
            f.close()
            return True

        elif self.board.can_claim_threefold_repetition():
            f.write("\nDraw by repetition\n")
            f.close()
            return True
        f.close()
        return False

    def play(self):

        self.board = ch.Board()
        self.game = pgn.Game()
        self.game.headers["Event"] = "Engine vs Engine"
        self.game.headers["Site"] = "Local"
        self.game.headers["Date"] = datetime.today().strftime('%Y-%m-%d')
        self.game.headers["Round"] = "0"
        self.game.headers["White"] = str(self.chess_engine_white)
        self.game.headers["Black"] = str(self.chess_engine_black)

        playing = True
        n = 0
        while playing:
            n +=1
            print(n)
            if self.game_finished():
                f = open("Results.txt", "a")
                f.write(str(self.game))
                f.write(str(self.board) + "\n")
                f.write(str(self.board.fen()) + "\n")
                f.close()
                playing = False
            elif self.board.turn == ch.WHITE:
                self.white_engine_choose_move()
            else:
                self.black_engine_choose_move()
