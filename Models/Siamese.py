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

class Siamese(nn.Module):
    def __init__(self):
        super(Siamese, self).__init__()

        self.seq_forward = nn.Sequential(
            nn.Linear(200, 400),
            nn.BatchNorm1d(400),
            nn.LeakyReLU(),
            nn.Linear(400, 200),
            nn.BatchNorm1d(200),
            nn.LeakyReLU(),
            nn.Linear(200, 100),
            nn.BatchNorm1d(100),
            nn.LeakyReLU(),
            nn.Linear(100, 2),
            nn.BatchNorm1d(2),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        output = self.seq_forward(x)
        return output

class GamesDataset(Dataset):
    def __init__(self, dataset1, dataset2):

        axis_x1 = []
        axis_x2 = []
        axis_y = []

        for i in range(len(dataset1)):
            order = np.random.randint(0,2)
            if order == 0:
                axis_x1.append(dataset1[i])
                axis_x2.append(dataset2[i])
                axis_y.append(np.array([1, 0]))
            else:
                axis_x1.append(dataset2[i])
                axis_x2.append(dataset1[i])
                axis_y.append(np.array([0, 1]))


        self.x1 = torch.from_numpy(np.array(axis_x1)).type(torch.FloatTensor)
        self.x2 = torch.from_numpy(np.array(axis_x2)).type(torch.FloatTensor)
        self.y = torch.from_numpy(np.array(axis_y)).type(torch.FloatTensor)
        self.n_samples = dataset1.shape[0]
    
    def __getitem__(self, index):
        return self.x1[index], self.x2[index], self.y[index]

    def __len__(self):
        return self.n_samples
