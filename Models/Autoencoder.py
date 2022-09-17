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
import time

start_time = time.time()


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

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
        return decoded, encodeds

class GamesDataset(Dataset):
    def __init__(self):
        games = np.load('Data\data_bits_normal.npy')
        self.x = torch.from_numpy(games[:,0:773])
        self.y = torch.from_numpy(games[:,[773]])
        self.n_samples = games.shape[0]
    
    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples

def loss_function(recon_x, x):
    BCE = F.binary_cross_entropy(recon_x, x.view(-1, 773), size_average=False)
    return BCE

def mse_loss_function(recon_x, x):
    MSE = F.mse_loss(recon_x, x.view(-1, 773), size_average=False)
    return MSE

dataset = GamesDataset()
dataLoader = DataLoader(dataset=dataset, batch_size=256, shuffle=True)

dataiter = iter(dataLoader)
positions, labels = dataiter.next()
print(torch.min(positions), torch.max(positions))

model = Autoencoder().to(device)
# criterion = nn.MSELoss()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

num_epochs = 10
outputs = []
model.train()
print("Start Training")
for epoch in range(num_epochs):
    train = 0
    for (pos,_) in dataLoader:
        
        if train%1000==0:
            if epoch==0:
                print(train, train*100/13600)
            else:
                print(f"Epoch: {epoch+1}, Loss: {loss.item():4f}, {train}, {train*100/54400}")

        pos = pos.to(device)

        
        
        recon, code = model(pos)
        loss = criterion(recon, pos)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train += 1
    
    for params in optimizer.param_groups:
        params['lr'] *= 0.98

    print(f"Epoch: {epoch+1}, Loss: {loss.item():4f}")
    outputs.append((epoch, pos, recon, code))

# pos, result = dataset[3]
# recon, code = model(pos)

# bit_board = recon.cpu().detach().numpy()

# bit_int = np.rint(bit_board).astype(int)

# print(bit_int)
# print(pos)

print("--- %s seconds ---" % (time.time() - start_time))