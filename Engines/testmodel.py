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


class TestModel:

    def __init__(self):
        self.depth_lim = 1

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        checkpoint = torch.load("Models\checkpointNewCCRL.pth")

        self.DBN = Autoencoder()
        self.DBN.load_state_dict(checkpoint['modelAE_state_dict'])
        self.DBN.to(self.device)
        self.DBN.eval()

        self.Siamese = Siamese()
        self.Siamese.load_state_dict(checkpoint['model_state_dict'])
        self.Siamese.to(self.device)
        self.Siamese.eval()

        print(checkpoint['epoch'], checkpoint['loss'])

    def get_bitboard(self, board):

        bitboard = np.zeros(773, dtype=int)

        piece_idx = {ch.PAWN: 0, ch.KNIGHT: 1, ch.BISHOP: 2, ch.ROOK: 3, ch.QUEEN: 4, ch.KING: 5}

        for i in range(64):
            if board.piece_at(i):
                color = int(board.piece_at(i).color)
                piece = 6 * color + piece_idx[board.piece_at(i).piece_type]
                bitboard[piece + 12 * i] = 1

        bitboard[-1] = int(board.turn)
        bitboard[-2] = int(board.has_kingside_castling_rights(ch.WHITE))
        bitboard[-3] = int(board.has_kingside_castling_rights(ch.BLACK))
        bitboard[-4] = int(board.has_queenside_castling_rights(ch.WHITE))
        bitboard[-5] = int(board.has_queenside_castling_rights(ch.BLACK))

        bitboard2D = np.array([bitboard])

        return bitboard2D

    def compare_positions(self, board1, board2):
        bitboard1 = self.get_bitboard(board1)

        recon, encode1 = self.DBN(torch.from_numpy(bitboard1).type(torch.FloatTensor).to(self.device))

        bitboard2 = self.get_bitboard(board2)

        recon, encode2 = self.DBN(torch.from_numpy(bitboard2).type(torch.FloatTensor).to(self.device))

        input = torch.cat((encode1, encode2), 1)

        output = self.Siamese(input)

        result = output.cpu().detach().numpy()

        return result[0]