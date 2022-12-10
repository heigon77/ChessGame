import chess as ch
import random as rd
import pandas as pd
import numpy as np
import torch
import torch.utils.data
from torch import nn, optim
from torch.nn import functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
from torchvision.utils import save_image

class Autoencoder(nn.Module):
    def __init__(self):
        super(Autoencoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(773, 600),
            nn.BatchNorm1d(600),
            nn.ReLU(),
            nn.Linear(600, 400),
            nn.BatchNorm1d(400),
            nn.ReLU(),
            nn.Linear(400, 200),
            nn.BatchNorm1d(200),
            nn.ReLU(),
            nn.Linear(200, 100),
            nn.BatchNorm1d(100),
            nn.ReLU()
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(100, 200),
            nn.BatchNorm1d(200),
            nn.ReLU(),
            nn.Linear(200, 400),
            nn.BatchNorm1d(400),
            nn.ReLU(),
            nn.Linear(400, 600),
            nn.BatchNorm1d(600),
            nn.ReLU(),
            nn.Linear(600, 773),
            nn.BatchNorm1d(773),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded, encoded

class GamesDataset(Dataset):
    def __init__(self, games):
        self.x = torch.from_numpy(games[:,0:773]).type(torch.FloatTensor)
        self.y = torch.from_numpy(games[:,[773]]).type(torch.FloatTensor)
        self.n_samples = games.shape[0]
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples
