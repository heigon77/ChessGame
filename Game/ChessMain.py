import sys
import pygame as pg
import chess as ch
import random as rd


class Game:

    def __init__(self):
        self.cyan_square = None
        self.screen = pg.display.set_mode((960, 960))
        self.boardStart_y = 0
        self.boardStart_x = 0
        self.square_size = 120
        self.white_queen = None
        self.white_king = None
        self.white_bishop = None
        self.white_knight = None
        self.white_rook = None
        self.white_pawn = None
        self.black_queen = None
        self.black_king = None
        self.black_bishop = None
        self.black_knight = None
        self.black_rook = None
        self.black_pawn = None
        self.brown_square = None
        self.white_square = None

        self.squares = []

        idx = 0
        for i in range(8):
            l_aux = []
            for j in range(8):
                l_aux.append(idx)
                idx += 1
            self.squares.insert(0, l_aux)

    def ConvertToScreenCoords(self, chessSquareList):
        # converts a (row,col) chessSquare into the pixel location of the upper-left corner of the square
        row = chessSquareList[0]
        col = chessSquareList[1]
        screenX = self.boardStart_x + col * self.square_size
        screenY = self.boardStart_y + row * self.square_size
        return [screenX, screenY]

    def ConvertToChessCoords(self, screenPositionList):
        # converts a screen pixel location (X,Y) into a chessSquare tuple (row,col)
        # x is horizontal, y is vertical
        # (x=0,y=0) is upper-left corner of the screen
        X = screenPositionList[0]
        Y = screenPositionList[1]
        row = (Y - self.boardStart_y) // self.square_size
        col = (X - self.boardStart_x) // self.square_size
        return [row, col]

    def loadImage(self):
        self.white_square = pg.image.load("Assets/white_square.png").convert()
        self.white_square = pg.transform.scale(self.white_square, (self.square_size, self.square_size))

        self.brown_square = pg.image.load("Assets/brown_square.png").convert()
        self.brown_square = pg.transform.scale(self.brown_square, (self.square_size, self.square_size))

        self.cyan_square = pg.image.load("Assets/cyan_square.png").convert()
        self.cyan_square = pg.transform.scale(self.cyan_square, (self.square_size, self.square_size))

        self.black_pawn = pg.image.load("Assets/Black/Chess_tile_pd.png").convert()
        self.black_pawn = pg.transform.scale(self.black_pawn, (self.square_size, self.square_size))
        self.black_rook = pg.image.load("Assets/Black/Chess_tile_rd.png").convert()
        self.black_rook = pg.transform.scale(self.black_rook, (self.square_size, self.square_size))
        self.black_knight = pg.image.load("Assets/Black/Chess_tile_nd.png").convert()
        self.black_knight = pg.transform.scale(self.black_knight, (self.square_size, self.square_size))
        self.black_bishop = pg.image.load("Assets/Black/Chess_tile_bd.png").convert()
        self.black_bishop = pg.transform.scale(self.black_bishop, (self.square_size, self.square_size))
        self.black_king = pg.image.load("Assets/Black/Chess_tile_kd.png").convert()
        self.black_king = pg.transform.scale(self.black_king, (self.square_size, self.square_size))
        self.black_queen = pg.image.load("Assets/Black/Chess_tile_qd.png").convert()
        self.black_queen = pg.transform.scale(self.black_queen, (self.square_size, self.square_size))

        self.white_pawn = pg.image.load("Assets/White/Chess_tile_pl.png").convert()
        self.white_pawn = pg.transform.scale(self.white_pawn, (self.square_size, self.square_size))
        self.white_rook = pg.image.load("Assets/White/Chess_tile_rl.png").convert()
        self.white_rook = pg.transform.scale(self.white_rook, (self.square_size, self.square_size))
        self.white_knight = pg.image.load("Assets/White/Chess_tile_nl.png").convert()
        self.white_knight = pg.transform.scale(self.white_knight, (self.square_size, self.square_size))
        self.white_bishop = pg.image.load("Assets/White/Chess_tile_bl.png").convert()
        self.white_bishop = pg.transform.scale(self.white_bishop, (self.square_size, self.square_size))
        self.white_king = pg.image.load("Assets/White/Chess_tile_kl.png").convert()
        self.white_king = pg.transform.scale(self.white_king, (self.square_size, self.square_size))
        self.white_queen = pg.image.load("Assets/White/Chess_tile_ql.png").convert()
        self.white_queen = pg.transform.scale(self.white_queen, (self.square_size, self.square_size))

    def play(self):
        pg.init()

        self.loadImage()

        board = ch.Board()

        fclick = None
        sclick = None

        playing = True

        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                if board.turn == ch.WHITE:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if fclick == None:
                            fclick = self.ConvertToChessCoords(pg.mouse.get_pos())
                        elif sclick == None:
                            sclick = self.ConvertToChessCoords(pg.mouse.get_pos())
                            move = ch.Move(self.squares[fclick[0]][fclick[1]], self.squares[sclick[0]][sclick[1]])
                            print(move)
                            if move in board.legal_moves:
                                board.push(move)
                                fclick = sclick = None
                                if board.is_checkmate():
                                    playing = False
                                    print("Checkmate")
                            else:
                                print("Invalid move")
                                fclick = sclick = None
                else:
                    moves = list(board.legal_moves)
                    board.push(rd.choice(moves))

            current_square = 0
            for r in range(8):
                for c in range(8):
                    screen = self.ConvertToScreenCoords([r, c])
                    if fclick == [r, c]:
                        self.screen.blit(self.cyan_square, (screen[0], screen[1]))
                        current_square = (current_square + 1) % 2
                    else:
                        if current_square:
                            self.screen.blit(self.brown_square, (screen[0], screen[1]))
                            current_square = (current_square + 1) % 2
                        else:
                            self.screen.blit(self.white_square, (screen[0], screen[1]))
                            current_square = (current_square + 1) % 2
                current_square = (current_square + 1) % 2

            for r in range(8):
                for c in range(8):
                    screen = self.ConvertToScreenCoords([r, c])
                    piece = board.piece_at(self.squares[r][c])
                    if piece is not None:
                        if piece.piece_type == ch.PAWN and piece.color == ch.BLACK:
                            self.screen.blit(self.black_pawn, (screen[0], screen[1]))
                        if piece.piece_type == ch.ROOK and piece.color == ch.BLACK:
                            self.screen.blit(self.black_rook, (screen[0], screen[1]))
                        if piece.piece_type == ch.KNIGHT and piece.color == ch.BLACK:
                            self.screen.blit(self.black_knight, (screen[0], screen[1]))
                        if piece.piece_type == ch.BISHOP and piece.color == ch.BLACK:
                            self.screen.blit(self.black_bishop, (screen[0], screen[1]))
                        if piece.piece_type == ch.QUEEN and piece.color == ch.BLACK:
                            self.screen.blit(self.black_queen, (screen[0], screen[1]))
                        if piece.piece_type == ch.KING and piece.color == ch.BLACK:
                            self.screen.blit(self.black_king, (screen[0], screen[1]))

                        if piece.piece_type == ch.PAWN and piece.color == ch.WHITE:
                            self.screen.blit(self.white_pawn, (screen[0], screen[1]))
                        if piece.piece_type == ch.ROOK and piece.color == ch.WHITE:
                            self.screen.blit(self.white_rook, (screen[0], screen[1]))
                        if piece.piece_type == ch.KNIGHT and piece.color == ch.WHITE:
                            self.screen.blit(self.white_knight, (screen[0], screen[1]))
                        if piece.piece_type == ch.BISHOP and piece.color == ch.WHITE:
                            self.screen.blit(self.white_bishop, (screen[0], screen[1]))
                        if piece.piece_type == ch.QUEEN and piece.color == ch.WHITE:
                            self.screen.blit(self.white_queen, (screen[0], screen[1]))
                        if piece.piece_type == ch.KING and piece.color == ch.WHITE:
                            self.screen.blit(self.white_king, (screen[0], screen[1]))

            pg.display.flip()
