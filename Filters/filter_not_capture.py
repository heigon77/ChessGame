import chess.pgn as chp
import chess as ch
import numpy as np
import random as rd

def get_bitboard(board):

    bitboard = np.zeros(773, dtype=int)

    piece_idx = {ch.PAWN: 0, ch.KNIGHT: 1, ch.BISHOP: 2, ch.ROOK: 3, ch.QUEEN: 4, ch.KING: 5}

    for i in range(64):
        if board.piece_at(i):
            color = int(board.piece_at(i).color)
            piece = 6*color + piece_idx[board.piece_at(i).piece_type]
            bitboard[piece + 12*i] = 1

    bitboard[-1] = int(board.turn)
    bitboard[-2] = int(board.has_kingside_castling_rights(ch.WHITE))
    bitboard[-3] = int(board.has_kingside_castling_rights(ch.BLACK))
    bitboard[-4] = int(board.has_queenside_castling_rights(ch.WHITE))
    bitboard[-5] = int(board.has_queenside_castling_rights(ch.BLACK))

    return bitboard

def get_result_draw(game):
    result = game.headers['Result']
    result = result.split('-')
    if result[0] == '1':
        return 1
    elif result[0] == '0':
        return -1
    else:
        return 0

def get_result(game):
    result = game.headers['Result']
    result = result.split('-')
    if result[0] == '1':
        return 1
    else:
        return 0

games = open("Data/CCRL-4040.[1462263].pgn")

num_games = 0
num_active = 0
f = open("Data/data_bits_normal_not_capture_computerchess30.csv", "w")

for i in range(1462262):
    if num_games % 1000 == 0:
        print(num_games, num_games * 100 / 1462262, num_active)
        
    bitboards = []
    num_games += 1

    game = chp.read_game(games)

    result = get_result(game)

    try:
        rating = (int(game.headers["WhiteElo"]) + int(game.headers["BlackElo"]))//2
    except KeyError:
        try:
            rating = int(game.headers["WhiteElo"])
        except KeyError:
            try:
                rating = int(game.headers["BlackElo"])
            except KeyError:
                rating = 0

    len_bits = len(list(game.mainline_moves()))-2

    if (len_bits >= 12 and rating > 3000 and "1/2" not in game.headers["Result"]):
        num_active += 1

        board = game.board()

        num_move = 0
        captures = []

        for move in game.mainline_moves():

            if(board.is_capture(move)):
                captures.append(num_move)
 
            board.push(move)
            bitboard = get_bitboard(board)
            bitboards.append(bitboard)

            num_move += 1
        
        pos = [0] * 6

        pos[0] = rd.randint(4, 2*len_bits//3)
        tries = 0 
        while (pos[0] in captures and tries < 10):
            tries += 1
            pos[0] = rd.randint(5, 2*len_bits//3)

        pos[1] = rd.randint((len_bits//3)+1,2*len_bits//3)
        tries = 0 
        while (pos[1] in captures and tries < 10):
            tries += 1
            pos[1] = rd.randint((len_bits//3)+1,2*len_bits//3)

        pos[2] = rd.randint((len_bits//3)+1,2*len_bits//3)
        tries = 0 
        while (pos[2]==pos[1] and pos[2] in captures and tries < 10):
            tries += 1
            pos[2] = rd.randint((len_bits//3)+1,2*len_bits//3)

        pos[3] = rd.randint((2*len_bits//3)+1,len_bits)
        tries = 0 
        while (pos[3] in captures and tries < 10):
            tries += 1
            pos[3] = rd.randint((2*len_bits//3)+1,len_bits)


        pos[4] = rd.randint((2*len_bits//3)+1,len_bits)
        tries = 0 
        while (pos[4]==pos[3] and pos[4] in captures and tries < 10):
            tries += 1
            pos[4] = rd.randint((2*len_bits//3)+1,len_bits)
        
        pos[5] = len_bits + 1
        pos.sort()

        for i in pos:
            for j in range(len(bitboards[i])-1):
                f.write(f"{bitboards[i][j]} ")
            f.write(f"{bitboards[i][-1]}")
            f.write(f",{result},")
            f.write(f"{i in captures}\n")



f.close()
