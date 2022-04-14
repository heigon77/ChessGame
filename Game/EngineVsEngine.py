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
        move = self.chess_engine_white.choose_move(self.board)
        if move:
            self.board.push(move)

        return

    def black_engine_choose_move(self):
        """
        The black engine update the board
        :return:
        """
        move = self.chess_engine_black.choose_move(self.board)
        if move:
            self.board.push(move)

        return

    def game_finished(self):
        """
        Verifies is the game ended
        :return:
        """

        if self.board.is_checkmate():
            print("Checkmate")
            return True

        elif self.board.is_stalemate():
            print("Stalemate")
            return True

        elif self.board.is_insufficient_material():
            print("Draw by insufficient material")
            return True

        elif self.board.can_claim_threefold_repetition():
            print("Draw by repetition")
            return True

        return False

    def play(self):

        for i in range(10):
            self.board = ch.Board()
            playing = True
            while playing:
                if self.game_finished():
                    playing = False
                elif self.board.turn == ch.WHITE:
                    self.white_engine_choose_move()
                else:
                    self.black_engine_choose_move()
