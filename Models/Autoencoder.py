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
            nn.LeakyReLU(),
            nn.Linear(600, 400),
            nn.BatchNorm1d(400),
            nn.LeakyReLU(),
            nn.Linear(400, 200),
            nn.BatchNorm1d(200),
            nn.LeakyReLU(),
            nn.Linear(200, 100),
            nn.BatchNorm1d(100),
            nn.LeakyReLU()
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(100, 200),
            nn.BatchNorm1d(200),
            nn.LeakyReLU(),
            nn.Linear(200, 400),
            nn.BatchNorm1d(400),
            nn.LeakyReLU(),
            nn.Linear(400, 600),
            nn.BatchNorm1d(600),
            nn.LeakyReLU(),
            nn.Linear(600, 773),
            nn.BatchNorm1d(773),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded, encoded

class GamesDatasetTrain(Dataset):
    def __init__(self, dataset):
        self.x = torch.from_numpy(dataset[:,0:773])
        self.y = torch.from_numpy(dataset[:,[773]])
        self.n_samples = dataset.shape[0]
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples

class GamesDatasetTest(Dataset):
    def __init__(self, dataset):
        self.x = torch.from_numpy(dataset[:,0:773])
        self.y = torch.from_numpy(dataset[:,[773]])
        self.n_samples = dataset.shape[0]
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples