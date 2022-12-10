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

games = open("Data\CCRL-4040.[1462263].pgn")

num_games = 0
num_active = 0
# f = open("Data/data_bits_normal.csv", "w")

for i in range(149283):
    if num_games % 1000 == 0:
        print(num_games, num_games * 100 / 149283, num_active)
        
    bitboards = []
    num_games += 1

    game = chp.read_game(games)

    result = get_result(game)

    rating = (int(game.headers["WhiteElo"]) + int(game.headers["BlackElo"]))//2

    len_bits = len(list(game.mainline_moves()))-2

    if (len_bits >= 14 and "Bullet" not in game.headers["Event"] and rating > 2400 and "1/2" not in game.headers["Result"] and "Normal" ==  game.headers["Termination"]):
        num_active += 1

        # board = game.board()

        # pos = [0] * 6

        # pos[0] = rd.randint(2, len_bits//3)

        # pos[1] = rd.randint((len_bits//3)+1,2*len_bits//3)
        # pos[2] = rd.randint((len_bits//3)+1,2*len_bits//3) 
        # while (pos[2]==pos[1]):
        #     pos[2] = rd.randint((len_bits//3)+1,2*len_bits//3)

        # pos[3] = rd.randint((2*len_bits//3)+1,len_bits)
        # pos[4] = rd.randint((2*len_bits//3)+1,len_bits)
        # while (pos[4]==pos[3]):
        #     pos[4] = rd.randint((2*len_bits//3)+1,len_bits)
        
        # pos[5] = len_bits + 1
        # pos.sort()

        # should_get = 0
        # ind = 0
        # for move in game.mainline_moves():
        #     board.push(move)

        #     if(should_get == pos[ind]):
        #         ind += 1
        #         bitboard = get_bitboard(board)
        #         bitboards.append(bitboard)

        #     should_get += 1
            
        # for bitboard in bitboards:
        #     for j in range(len(bitboard)-1):
        #         f.write(f"{bitboard[j]} ")
        #     f.write(f"{bitboard[-1]}")
        #     f.write(f",{result}\n")

f.close()
