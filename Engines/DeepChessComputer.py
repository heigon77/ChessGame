import chess as ch
import random as rd
import numpy as np

import torch
import torch.utils.data
from torch import nn, optim
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
from torchvision.utils import save_image
import time

from Models.Autoencoder import Autoencoder
from Models.Siamese import Siamese


class DeepChessComputer:

    def __init__(self):
        self.depth_lim = 3

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        checkpoint = torch.load("Models\Checkpoint\checkpointDeepChessComputerChess200.pth")

        self.DBN = Autoencoder()
        self.DBN.load_state_dict(checkpoint['modelAE_state_dict'])
        self.DBN.to(self.device)
        self.DBN.eval()

        self.Siamese = Siamese()
        self.Siamese.load_state_dict(checkpoint['model_state_dict'])
        self.Siamese.to(self.device)
        self.Siamese.eval()

        # print(checkpoint['epoch'], checkpoint['loss'])

        self.castled = False
    
    def __str__(self):
        return "DeepChessComputer"

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

        score, move = self.alphabeta(board, self.depth_lim, -100, 100, max_player, board)


        # print("Escolhido: ", score, move)

        return move
    
    def get_bitboard(self, board):

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

        bitboard2D = np.array([bitboard])

        return bitboard2D
    
    def alphabeta(self, board, depth, alpha, beta, white, orig_board):

        if depth == 0:
            return self.compare_positions(board, orig_board), None

        if white:

            v = -100
            moves = board.legal_moves
            moves = list(moves)
            best_move = None

            for move in moves:

                new_board = board.copy()
                new_board.push(move)
                candidate_v, _ = self.alphabeta(new_board, depth - 1, alpha, beta, False, orig_board)

                if candidate_v >= v:
                    v = candidate_v
                    best_move = move
                else:
                    pass

                alpha = max(alpha, v)

                if beta <= alpha:
                    break
                
            return v, best_move

        else:

            v = 100
            moves = board.legal_moves
            moves = list(moves)
            best_move = None

            for move in moves:

                new_board = board.copy()
                new_board.push(move)
                candidate_v, _ = self.alphabeta(new_board, depth - 1, alpha, beta, True, orig_board)

                if candidate_v <= v:
                    v = candidate_v
                    best_move = move
                else:
                    pass

                beta = min(beta, v)

                if beta <= alpha:
                    break

            return v, best_move
    
    def compare_positions(self, board1, board2):
        bitboard1 = self.get_bitboard(board1)

        recon, encode1 = self.DBN(torch.from_numpy(bitboard1).type(torch.FloatTensor).to(self.device))

        bitboard2 = self.get_bitboard(board2)

        recon, encode2 = self.DBN(torch.from_numpy(bitboard2).type(torch.FloatTensor).to(self.device))

        input = torch.cat((encode1, encode2), 1)

        output = self.Siamese(input)

        result = output.cpu().detach().numpy()

        return result[0][0]

