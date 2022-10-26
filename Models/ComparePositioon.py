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

from Autoencoder import Autoencoder
from Siamese import Siamese

def get_bitboard( board):

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


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

checkpoint = torch.load("Models\checkpoint.pth")

dbn = Autoencoder()
dbn.load_state_dict(checkpoint['modelAE_state_dict'])
dbn.to(device)
dbn.eval()

Siamese = Siamese()
Siamese.load_state_dict(checkpoint['model_state_dict'])
Siamese.to(device)
Siamese.eval()

board2 = "r2q1bnr/pppbk1pp/5pn1/3Pp3/5Q2/2PBBN2/PP4PP/RN2K2R w KQ - 0 1"

board1 = "r2qkbnr/pppb2pp/5pn1/3P4/5p2/2PBBN2/PP4PP/RN2K2R w KQkq - 0 1"

worseBoard = ch.Board(fen=board1)
betterBoard = ch.Board(fen=board2)

bitboard1 = get_bitboard(worseBoard)

recon, encode1 = dbn(torch.from_numpy(bitboard1).type(torch.FloatTensor).to(device))

bitboard2 = get_bitboard(betterBoard)

recon, encode2 = dbn(torch.from_numpy(bitboard2).type(torch.FloatTensor).to(device))

input = torch.cat((encode1, encode2), 1)

output = Siamese(input)

print(output.cpu())

if (output.cpu().detach().numpy()[0] > .5).astype(int)[0] == 1:
    trade = True
else:
    trade = False

print(trade)

