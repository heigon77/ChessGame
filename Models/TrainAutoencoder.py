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

from Autoencoder import Autoencoder, GamesDatasetTest, GamesDatasetTrain

start_time = time.time()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
np.random.seed(42)

print("Loading Data")
games = np.load('Data\data_bits_normal.npy')
np.random.shuffle(games)

datasetTrain = GamesDatasetTrain(games[:int(len(games)*.8)])
dataLoaderTrain = DataLoader(dataset=datasetTrain, batch_size=256)

datasetTest = GamesDatasetTest(games[int(len(games)*.8):])
dataLoaderTest = DataLoader(dataset=datasetTest, batch_size=256)

print(f"Train: {len(dataLoaderTrain.dataset)}")
print(f"Test: {len(dataLoaderTest.dataset)}")

model = Autoencoder().to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.005)

num_epochs = 2
outputs = []
model.train()
print("Start Training")
for epoch in range(num_epochs):

    for (pos,_) in dataLoaderTrain:   
        pos = pos.to(device)

        recon, code = model(pos)
        loss = criterion(recon, pos)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    for params in optimizer.param_groups:
        params['lr'] *= 0.98

    print(f"Epoch: {epoch+1}, Loss: {loss.item():4f}")
    outputs.append((epoch, pos, recon, code))
print("Finish Training")

model.eval()
print("Start Testing")
test_loss_mse = 0
total_diff = 0
total_diff_int = 0
with torch.no_grad():
    for (pos,_) in dataLoaderTest:
        pos = pos.to(device)
        posnp = pos.cpu().detach().numpy()

        recon, code = model(pos)
        
        pred = (recon.cpu().detach().numpy() > .5).astype(int)
        total_diff += float(np.sum(posnp != pred))
        total_diff_int += int(not np.array_equal(posnp,pred))
        test_loss_mse += criterion(recon, pos).item()

test_loss_mse /= len(dataLoaderTest.dataset)
total_diff_all = total_diff / len(dataLoaderTest.dataset)
total_diff_percent = total_diff_int * 100 / len(dataLoaderTest.dataset)
print(f"====> Test set loss (mse): {test_loss_mse}")
print(f"====> Test set diff: {total_diff_all}")
print(f"====> Test set diff perccentage: {total_diff_percent}")
print("Finish Testing")

print("Saving model")
torch.save(model.state_dict(), "Models\Autoencoder.pth")

runningTime = (time.time() - start_time)
print(f"--- {runningTime:2f}s seconds ---")