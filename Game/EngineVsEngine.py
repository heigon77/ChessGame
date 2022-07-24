import chess as ch


class EngineVsEngine:

    def __init__(self, chess_engine_black, chess_engine_white):
        self.chess_engine_black = chess_engine_black
        self.chess_engine_white = chess_engine_white
        self.board = None

    def white_engine_choose_move(self):
        """
        The white engine update the board
        :return:
        """
        move = self.chess_engine_white.choose_move(self.board, ch.WHITE)
        if move:
            self.board.push(move)

        return

    def black_engine_choose_move(self):
        """
        The black engine update the board
        :return:
        """
        move = self.chess_engine_black.choose_move(self.board, ch.BLACK)
        if move:
            self.board.push(move)

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

        for i in range(4):

            self.board = ch.Board()
            playing = True
            while playing:
                if self.game_finished():
                    f = open("Results.txt", "a")
                    f.write(str(self.board) + "\n")
                    f.write(str(self.board.fen()) + "\n")
                    f.close()
                    playing = False
                elif self.board.turn == ch.WHITE:
                    self.white_engine_choose_move()
                else:
                    self.black_engine_choose_move()
