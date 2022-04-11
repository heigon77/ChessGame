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

        self.boardStart = [0, 0]
        self.square_size = 120

        self.squares = []

        idx = 0
        for i in range(8):
            l_aux = []
            for j in range(8):
                l_aux.append(idx)
                idx += 1
            self.squares.insert(0, l_aux)

    def ConvertToScreenCoord(self, chessSquareList):
        # converts a (row,col) chessSquare into the pixel location of the upper-left corner of the square
        screen = [self.boardStart[0] + chessSquareList[1] * self.square_size,
                  self.boardStart[1] + chessSquareList[0] * self.square_size]
        return screen

    def ConvertToChessCoord(self, screenPositionList):
        # converts a screen pixel location (X,Y) into a chessSquare tuple (row,col)
        # x is horizontal, y is vertical
        # (x=0,y=0) is upper-left corner of the screen
        chess = [(screenPositionList[1] - self.boardStart[1]) // self.square_size,
                 (screenPositionList[0] - self.boardStart[0]) // self.square_size]
        return chess

    def LoadImage(self):

        self.square_color_dict = {
            "white": pg.transform.scale(pg.image.load("Assets/white_square.png").convert()
                                        , (self.square_size, self.square_size)),
            "brown": pg.transform.scale(pg.image.load("Assets/brown_square.png").convert()
                                        , (self.square_size, self.square_size)),
            "cyan": pg.transform.scale(pg.image.load("Assets/cyan_square.png").convert()
                                       , (self.square_size, self.square_size))
        }

        self.black_pieces_dict = {
            "pawn": pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_pd.png").convert()
                                       , (self.square_size, self.square_size)),
            "rook": pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_rd.png").convert()
                                       , (self.square_size, self.square_size)),
            "knight": pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_nd.png").convert()
                                         , (self.square_size, self.square_size)),
            "bishop": pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_bd.png").convert()
                                         , (self.square_size, self.square_size)),
            "king": pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_kd.png").convert()
                                       , (self.square_size, self.square_size)),
            "queen": pg.transform.scale(pg.image.load("Assets/Black/Chess_tile_qd.png").convert()
                                        , (self.square_size, self.square_size))
        }

        self.white_pieces_dict = {
            "pawn": pg.transform.scale(pg.image.load("Assets/White/Chess_tile_pl.png").convert()
                                       , (self.square_size, self.square_size)),
            "rook": pg.transform.scale(pg.image.load("Assets/White/Chess_tile_rl.png").convert()
                                       , (self.square_size, self.square_size)),
            "knight": pg.transform.scale(pg.image.load("Assets/White/Chess_tile_nl.png").convert()
                                         , (self.square_size, self.square_size)),
            "bishop": pg.transform.scale(pg.image.load("Assets/White/Chess_tile_bl.png").convert()
                                         , (self.square_size, self.square_size)),
            "king": pg.transform.scale(pg.image.load("Assets/White/Chess_tile_kl.png").convert()
                                       , (self.square_size, self.square_size)),
            "queen": pg.transform.scale(pg.image.load("Assets/White/Chess_tile_ql.png").convert()
                                        , (self.square_size, self.square_size))
        }

    def play(self):
        pg.init()

        self.LoadImage()

        board = ch.Board()

        fir_click = None
        sec_click = None

        playing = True

        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                if board.turn == ch.WHITE:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if fir_click is None:
                            fir_click = self.ConvertToChessCoord(pg.mouse.get_pos())
                        elif sec_click is None:
                            sec_click = self.ConvertToChessCoord(pg.mouse.get_pos())

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
                                if board.is_checkmate() or board.is_stalemate():
                                    playing = False
                                    print("Checkmate")
                            else:
                                print("Invalid move")
                                print(board.legal_moves)
                                fir_click = sec_click = None
                else:
                    if board.is_checkmate() or board.is_stalemate():
                        playing = False
                        print("Checkmate")
                    moves = list(board.legal_moves)
                    if moves:
                        board.push(rd.choice(moves))

            current_square = 0
            for r in range(8):
                for c in range(8):
                    screen = self.ConvertToScreenCoord([r, c])
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
                    screen = self.ConvertToScreenCoord([r, c])
                    piece = board.piece_at(self.squares[r][c])
                    if piece is not None:
                        if piece.piece_type == ch.PAWN and piece.color == ch.BLACK:
                            self.screen.blit(self.black_pieces_dict["pawn"], (screen[0], screen[1]))
                        if piece.piece_type == ch.ROOK and piece.color == ch.BLACK:
                            self.screen.blit(self.black_pieces_dict["rook"], (screen[0], screen[1]))
                        if piece.piece_type == ch.KNIGHT and piece.color == ch.BLACK:
                            self.screen.blit(self.black_pieces_dict["knight"], (screen[0], screen[1]))
                        if piece.piece_type == ch.BISHOP and piece.color == ch.BLACK:
                            self.screen.blit(self.black_pieces_dict["bishop"], (screen[0], screen[1]))
                        if piece.piece_type == ch.QUEEN and piece.color == ch.BLACK:
                            self.screen.blit(self.black_pieces_dict["queen"], (screen[0], screen[1]))
                        if piece.piece_type == ch.KING and piece.color == ch.BLACK:
                            self.screen.blit(self.black_pieces_dict["king"], (screen[0], screen[1]))

                        if piece.piece_type == ch.PAWN and piece.color == ch.WHITE:
                            self.screen.blit(self.white_pieces_dict["pawn"], (screen[0], screen[1]))
                        if piece.piece_type == ch.ROOK and piece.color == ch.WHITE:
                            self.screen.blit(self.white_pieces_dict["rook"], (screen[0], screen[1]))
                        if piece.piece_type == ch.KNIGHT and piece.color == ch.WHITE:
                            self.screen.blit(self.white_pieces_dict["knight"], (screen[0], screen[1]))
                        if piece.piece_type == ch.BISHOP and piece.color == ch.WHITE:
                            self.screen.blit(self.white_pieces_dict["bishop"], (screen[0], screen[1]))
                        if piece.piece_type == ch.QUEEN and piece.color == ch.WHITE:
                            self.screen.blit(self.white_pieces_dict["queen"], (screen[0], screen[1]))
                        if piece.piece_type == ch.KING and piece.color == ch.WHITE:
                            self.screen.blit(self.white_pieces_dict["king"], (screen[0], screen[1]))

            pg.display.flip()
