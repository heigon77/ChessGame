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

from Siamese import Siamese, GamesDataset

start_time = time.time()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
np.random.seed(42)

model = Siamese().to(device)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

num_epochs = 10
model.train()

games_wins = np.load('Data\data_bits_normal_wins_train.npy')
games_wins_crop = games_wins[np.random.choice(len(games_wins), size=1000000, replace=False)]

games_loss = np.load('Data\data_bits_normal_loss_train.npy')
games_loss_crop = games_loss[np.random.choice(len(games_loss), size=1000000, replace=False)]

datasetTrain = GamesDataset(games_wins_crop, games_loss_crop )
dataLoaderTrain = DataLoader(dataset=datasetTrain, batch_size=64)


print("Start Training")
for epoch in range(num_epochs):


    for (pos,res) in dataLoaderTrain:
        
        pos = pos.to(device)
        res = res.to(device)

        
        out = model(pos)
        loss = criterion(out, res)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    for params in optimizer.param_groups:
        params['lr'] *= 0.99

    print(f"Epoch: {epoch+1}, Loss: {loss.item():4f}")

print("Finish Training")

model.eval()
print("Start Testing")
test_loss = 0
total = 0
right = 0
with torch.no_grad():
    games_wins = np.load('Data\data_bits_normal_wins_test.npy').astype(float)
    games_wins_crop = games_wins[np.random.choice(len(games_wins), size=1000, replace=False)]

    games_loss = np.load('Data\data_bits_normal_loss_test.npy').astype(float)
    games_loss_crop = games_loss[np.random.choice(len(games_loss), size=1000, replace=False)]

    datasetTest = GamesDataset(games_wins_crop, games_loss_crop )
    dataLoaderTest = DataLoader(dataset=datasetTest, batch_size=64)

    for (pos,res) in dataLoaderTest:

  
        pos = pos.to(device)
        res = res.to(device)

        out = model(pos)
        
        test_loss += criterion(out, res).item()

        pred = (out.cpu().detach().numpy() > .5).astype(int)
        corr = res.cpu().detach().numpy().astype(int)
        # print("Corr", corr)
        # print("Pred", pred)
        for i in range(len(pred)):
            total += 1
            right += np.array_equal(corr[i],pred[i])

test_loss /= len(dataLoaderTest.dataset)
accuracy = right/total * 100

print(f"====> Test set loss: {test_loss}")
print(f"====> Test set accuracy: {accuracy}")

print("Finish Testing")

print("Saving model")
torch.save(model.state_dict(), "Models\SiameseOver.pth")

runningTime = (time.time() - start_time)
print(f"--- {runningTime:2f}s seconds ---")