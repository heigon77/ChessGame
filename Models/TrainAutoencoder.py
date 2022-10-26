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

from Autoencoder import Autoencoder, GamesDataset

start_time = time.time()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
np.random.seed(42)

print("Loading Data")
games = np.load('Data\data_bits_normal.npy')
np.random.shuffle(games)

datasetTrain = GamesDataset(games[:int(len(games)*.98)])
dataLoaderTrain = DataLoader(dataset=datasetTrain, batch_size=64)

datasetTest = GamesDataset(games[int(len(games)*.98):])
dataLoaderTest = DataLoader(dataset=datasetTest, batch_size=64)

print(f"Train: {len(dataLoaderTrain.dataset)}")
print(f"Test: {len(dataLoaderTest.dataset)}")

model = Autoencoder().to(device)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)

num_epochs = 200
model.train()

PATH = 'checkpointDBN.pth'
file_out = open('Data/outputsDBN.csv','w')
file_out.write(f"Epoch,Loss\n")


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
    
    torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss
            }, PATH)

    print(f"Epoch: {epoch+1}, Loss: {loss.item():4f}")
    file_out.write(f"{epoch+1},{loss.item():4f}\n")
file_out.close()
print("Finish Training")

model.eval()
print("Start Testing")
test_loss_mse = 0
total_diff = 0
total_diff_int = 0
total = 0
right = 0
with torch.no_grad():
    for (pos,_) in dataLoaderTest:
        pos = pos.to(device)
        posnp = pos.cpu().detach().numpy()

        recon, code = model(pos)
        
        pred = (recon.cpu().detach().numpy() > .5).astype(int)
        total_diff += float(np.sum(posnp != pred))
        for i in range(len(pred)):
            total += 1
            right += np.array_equal(posnp[i],pred[i])
        test_loss_mse += criterion(recon, pos).item()

test_loss_mse /= len(dataLoaderTest.dataset)
total_diff_all = total_diff / len(dataLoaderTest.dataset)
total_diff_percent = right/total * 100
print(f"====> Test set loss (mse): {test_loss_mse}")
print(f"====> Test set diff: {total_diff_all}")
print(f"====> Test set diff perccentage: {total_diff_percent}")
print("Finish Testing")

print("Saving model")
torch.save(model.state_dict(), "Models\Autoencoder.pth")

runningTime = (time.time() - start_time)
print(f"--- {runningTime:2f}s seconds ---")