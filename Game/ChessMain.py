import sys
import pygame as pg
import chess as ch
import random as rd


class Game:

    def __init__(self):

        self.square_color_dict = None
        self.black_pieces_dict = None
        self.white_pieces_dict = None

        self.screen = pg.display.set_mode((960, 960))

        self.board_start = [0, 0]
        self.square_size = 120

        self.squares = []
        idx = 0
        for i in range(8):
            l_aux = []
            for j in range(8):
                l_aux.append(idx)
                idx += 1
            self.squares.insert(0, l_aux)

    def to_screen(self, chess_square_list):
        # converts a (row,col) chessSquare into the pixel location of the upper-left corner of the square
        screen = [self.board_start[0] + chess_square_list[1] * self.square_size,
                  self.board_start[1] + chess_square_list[0] * self.square_size]
        return screen

    def to_chess(self, screen_position_list):
        # converts a screen pixel location (X,Y) into a chessSquare tuple (row,col)
        # x is horizontal, y is vertical
        # (x=0,y=0) is upper-left corner of the screen
        chess = [(screen_position_list[1] - self.board_start[1]) // self.square_size,
                 (screen_position_list[0] - self.board_start[0]) // self.square_size]
        return chess

    def load_image(self):

        self.square_color_dict = {
            "white": pg.transform.scale(pg.image.load("Assets/white_square.png").convert()
                                        , (self.square_size, self.square_size)),
            "brown": pg.transform.scale(pg.image.load("Assets/brown_square.png").convert()
                                        , (self.square_size, self.square_size)),
            "cyan": pg.transform.scale(pg.image.load("Assets/cyan_square.png").convert()
                                       , (self.square_size, self.square_size))
        }

        self.black_pieces_dict = {
            ch.PAWN: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_pd.png").convert()
                                        , (self.square_size, self.square_size)),
            ch.ROOK: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_rd.png").convert()
                                        , (self.square_size, self.square_size)),
            ch.KNIGHT: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_nd.png").convert()
                                          , (self.square_size, self.square_size)),
            ch.BISHOP: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_bd.png").convert()
                                          , (self.square_size, self.square_size)),
            ch.KING: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_kd.png").convert()
                                        , (self.square_size, self.square_size)),
            ch.QUEEN: pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_qd.png").convert()
                                         , (self.square_size, self.square_size))
        }

        self.white_pieces_dict = {
            ch.PAWN: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_pl.png").convert()
                                        , (self.square_size, self.square_size)),
            ch.ROOK: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_rl.png").convert()
                                        , (self.square_size, self.square_size)),
            ch.KNIGHT: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_nl.png").convert()
                                          , (self.square_size, self.square_size)),
            ch.BISHOP: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_bl.png").convert()
                                          , (self.square_size, self.square_size)),
            ch.KING: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_kl.png").convert()
                                        , (self.square_size, self.square_size)),
            ch.QUEEN: pg.transform.scale(pg.image.load("Assets/White/Chess_tile_ql.png").convert()
                                         , (self.square_size, self.square_size))
        }

    def play(self):
        pg.init()

        self.load_image()

        board = ch.Board()

        fir_click = None
        sec_click = None

        playing = True
        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                elif board.is_checkmate():
                    playing = False
                    print("Checkmate")
                elif board.is_stalemate():
                    playing = False
                    print("Stalemate")
                elif board.turn == ch.WHITE:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if fir_click is None:
                            fir_click = self.to_chess(pg.mouse.get_pos())
                        elif sec_click is None:
                            sec_click = self.to_chess(pg.mouse.get_pos())

                            if (ch.Move(self.squares[fir_click[0]][fir_click[1]],
                                        self.squares[sec_click[0]][sec_click[1]],
                                        ch.QUEEN)) in board.legal_moves:
                                move = ch.Move(self.squares[fir_click[0]][fir_click[1]],
                                               self.squares[sec_click[0]][sec_click[1]],
                                               ch.QUEEN)
                            else:
                                move = ch.Move(self.squares[fir_click[0]][fir_click[1]],
                                               self.squares[sec_click[0]][sec_click[1]])

                            print(move)
                            if move in board.legal_moves:
                                board.push(move)
                                fir_click = sec_click = None
                            else:
                                print("Invalid move")
                                print(board.legal_moves)
                                fir_click = sec_click = None
                else:
                    moves = list(board.legal_moves)
                    if moves:
                        board.push(rd.choice(moves))

            current_square = 0
            for r in range(8):
                for c in range(8):
                    screen = self.to_screen([r, c])
                    if fir_click == [r, c]:
                        self.screen.blit(self.square_color_dict["cyan"], (screen[0], screen[1]))
                        current_square = (current_square + 1) % 2
                    else:
                        if current_square:
                            self.screen.blit(self.square_color_dict["brown"], (screen[0], screen[1]))
                            current_square = (current_square + 1) % 2
                        else:
                            self.screen.blit(self.square_color_dict["white"], (screen[0], screen[1]))
                            current_square = (current_square + 1) % 2
                current_square = (current_square + 1) % 2

            for r in range(8):
                for c in range(8):
                    screen = self.to_screen([r, c])
                    piece = board.piece_at(self.squares[r][c])
                    if piece is not None:
                        if piece.color == ch.BLACK:
                            self.screen.blit(self.black_pieces_dict[piece.piece_type], (screen[0], screen[1]))
                        else:
                            self.screen.blit(self.white_pieces_dict[piece.piece_type], (screen[0], screen[1]))

            pg.display.flip()
