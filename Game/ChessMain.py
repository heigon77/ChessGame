import sys
import pygame as pg
import chess as ch


class Game:

    def __init__(self, chess_engine, chess_dot_com=None):

        self.chess_engine = chess_engine
        self.chess_dot_com = chess_dot_com

        self.square_color_dict = None
        self.black_pieces_dict = None
        self.white_pieces_dict = None

        self.fir_click = None
        self.sec_click = None

        self.screen = pg.display.set_mode((1000, 1000))
        self.board = None
        self.board_start = [40, 0]
        self.square_size = 120

        # Creating the matrix with the int that represents each square in chess lib
        self.squares = []
        idx = 0
        for i in range(8):
            l_aux = []
            for j in range(8):
                l_aux.append(idx)
                idx += 1
            self.squares.insert(0, l_aux)

    def to_screen_coordinates(self, chess_square_list):
        """
        Converting chess square coordinates to screen position
        :param chess_square_list:
        :return screen_coordinates:
        """
        screen_coordinates = [self.board_start[0] + chess_square_list[1] * self.square_size,
                              self.board_start[1] + chess_square_list[0] * self.square_size]
        return screen_coordinates

    def to_chess_coordinates(self, screen_position_list):
        """
        Converting chess screen coordinates to chess coordinates
        :param screen_position_list:
        :return chess_coordinates:
        """
        chess_coordinates = [(screen_position_list[1] - self.board_start[1]) // self.square_size,
                             (screen_position_list[0] - self.board_start[0]) // self.square_size]
        return chess_coordinates

    def load_image(self):
        """
        Load all the image assets
        :return:
        """
        self.square_color_dict = {
            "light": pg.transform.scale(pg.image.load("Assets/Squares/light_square.png").convert(),
                                        (self.square_size, self.square_size)),
            "dark": pg.transform.scale(pg.image.load("Assets/Squares/dark_square.png").convert(),
                                       (self.square_size, self.square_size)),
            "selected": pg.transform.scale(pg.image.load("Assets/Squares/yellow_square.png").convert(),
                                           (self.square_size, self.square_size))

        }

        self.black_pieces_dict = {
            ch.PAWN: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_pd.png").convert(),
                                        (self.square_size, self.square_size)),
            ch.ROOK: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_rd.png").convert(),
                                        (self.square_size, self.square_size)),
            ch.KNIGHT: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_nd.png").convert(),
                                          (self.square_size, self.square_size)),
            ch.BISHOP: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_bd.png").convert(),
                                          (self.square_size, self.square_size)),
            ch.KING: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_kd.png").convert(),
                                        (self.square_size, self.square_size)),
            ch.QUEEN: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_qd.png").convert(),
                                         (self.square_size, self.square_size))
        }

        self.white_pieces_dict = {
            ch.PAWN: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_pl.png").convert(),
                                        (self.square_size, self.square_size)),
            ch.ROOK: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_rl.png").convert(),
                                        (self.square_size, self.square_size)),
            ch.KNIGHT: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_nl.png").convert(),
                                          (self.square_size, self.square_size)),
            ch.BISHOP: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_bl.png").convert(),
                                          (self.square_size, self.square_size)),
            ch.KING: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_kl.png").convert(),
                                        (self.square_size, self.square_size)),
            ch.QUEEN: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_ql.png").convert(),
                                         (self.square_size, self.square_size))
        }

        return

    def player_choose_move(self, event):
        """
        Get the event from pygame and the board and update it with the player move
        :param event:
        :return:
        """

        if event.type == pg.MOUSEBUTTONDOWN:

            if self.fir_click is None:
                self.fir_click = self.to_chess_coordinates(pg.mouse.get_pos())

            elif self.sec_click is None:
                self.sec_click = self.to_chess_coordinates(pg.mouse.get_pos())

                if (ch.Move(self.squares[self.fir_click[0]][self.fir_click[1]],
                            self.squares[self.sec_click[0]][self.sec_click[1]],
                            ch.QUEEN)) in self.board.legal_moves:
                    move = ch.Move(self.squares[self.fir_click[0]][self.fir_click[1]],
                                   self.squares[self.sec_click[0]][self.sec_click[1]],
                                   ch.QUEEN)
                else:
                    move = ch.Move(self.squares[self.fir_click[0]][self.fir_click[1]],
                                   self.squares[self.sec_click[0]][self.sec_click[1]])

                print(move)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.fir_click = self.sec_click = None
                else:
                    print("Invalid move")
                    print(self.board.legal_moves)
                    self.fir_click = self.sec_click = None
        return

    def engine_choose_move(self):
        """
        The engine update the board
        :return:
        """
        move = self.chess_engine.choose_move(self.board)
        if move:
            self.board.push(move)

        return

    def draw_chess_board(self):
        """
        Draw the board's squares
        :return:
        """

        # Create The Backgound
        background = pg.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        font = pg.font.Font(None, 64)

        chess_coluns = ["A", "B", "C", "D", "E", "F", "G", "H"]
        init_pos = 85
        for i in chess_coluns:
            text = font.render(i, True, (255, 255, 255))
            textpos = text.get_rect(x=init_pos, y=960)
            init_pos += 120
            background.blit(text, textpos)

        chess_rows = ["8", "7", "6", "5", "4", "3", "2", "1"]
        init_pos = 40
        for i in chess_rows:
            text = font.render(i, True, (255, 255, 255))
            textpos = text.get_rect(x=10, y=init_pos)
            init_pos += 120
            background.blit(text, textpos)

        self.screen.blit(background, (0, 0))

        current_square = 0

        for i in range(8):
            for j in range(8):
                screen_cd = self.to_screen_coordinates([i, j])
                if self.fir_click == [i, j]:
                    self.screen.blit(self.square_color_dict["selected"], (screen_cd[0], screen_cd[1]))
                    current_square = (current_square + 1) % 2
                else:
                    if current_square:
                        self.screen.blit(self.square_color_dict["dark"], (screen_cd[0], screen_cd[1]))
                        current_square = (current_square + 1) % 2
                    else:
                        self.screen.blit(self.square_color_dict["light"], (screen_cd[0], screen_cd[1]))
                        current_square = (current_square + 1) % 2
            current_square = (current_square + 1) % 2

        return

    def draw_pieces(self):
        """
        Draw the pieces on the board
        :return:
        """
        for i in range(8):
            for j in range(8):
                screen = self.to_screen_coordinates([i, j])
                piece = self.board.piece_at(self.squares[i][j])
                if piece is not None:
                    if piece.color == ch.BLACK:
                        self.screen.blit(self.black_pieces_dict[piece.piece_type], (screen[0], screen[1]))
                    else:
                        self.screen.blit(self.white_pieces_dict[piece.piece_type], (screen[0], screen[1]))
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

        return False

    def play(self):
        """
        Method that runs the game
        :return:
        """
        pg.init()
        pg.display.set_caption("Chess Game")

        self.load_image()

        self.board = ch.Board()

        if self.chess_dot_com is not None:
            daily_puzzle = self.chess_dot_com.get_daily_puzzle()
            self.board.set_fen(daily_puzzle.json['puzzle']['fen'])

        playing = True
        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                elif self.game_finished():
                    playing = False
                elif self.board.turn == ch.WHITE:
                    self.player_choose_move(event)
                else:
                    self.engine_choose_move()

            self.draw_chess_board()

            self.draw_pieces()

            pg.display.flip()
