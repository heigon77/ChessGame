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
from Autoencoder import Autoencoder

start_time = time.time()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
np.random.seed(42)



model = Siamese()
model.to(device)
model.train()

modelAE = Autoencoder()
checkpointDBN = torch.load("Models\Checkpoint\checkpointDBNlichessnormal.pth")
modelAE.load_state_dict(checkpointDBN['model_state_dict'])
modelAE.to(device)
modelAE.train()

criterion = nn.BCELoss()
optimizer = optim.Adam(list(model.parameters()) + list(modelAE.parameters()), lr=0.01)

PATH = "Models\Checkpoint\checkpointDeepChessComputerChess200.pth"
file_out = open('Data\outputsDeepChessComputerChess200.csv','w')
file_out.write(f"Epoch,Loss\n")

num_epochs = 200

print("Start Training")
for epoch in range(num_epochs):

    games_wins = np.load('Data\data_bits_normal_computerchess_wins_train.npy')
    games_wins_crop = games_wins[np.random.choice(len(games_wins), size=1000000, replace=False)]

    games_loss = np.load('Data\data_bits_normal_computerchess_loss_train.npy')
    games_loss_crop = games_loss[np.random.choice(len(games_loss), size=1000000, replace=False)]


    datasetTrain = GamesDataset(games_wins_crop, games_loss_crop )
    dataLoaderTrain = DataLoader(dataset=datasetTrain, batch_size=64)


    for (pos1,pos2,res) in dataLoaderTrain:
        
        pos1 = pos1.to(device)
        pos2 = pos2.to(device)
        res = res.to(device)

        _, encode1 = modelAE(pos1)
        _, encode2 = modelAE(pos2)

        input = torch.cat((encode1,encode2), 1)
        
        out = model(input)
        loss = criterion(out, res)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    for params in optimizer.param_groups:
        params['lr'] *= 0.99
    
    torch.save({
            'epoch': epoch,
            'modelAE_state_dict': modelAE.state_dict(),
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'loss': loss
            }, PATH)

    print(f"Epoch: {epoch+1}, Loss: {loss.item():4f}")
    file_out.write(f"{epoch+1},{loss.item():4f}\n")

file_out.close()
print("Finish Training")

model.eval()
modelAE.eval()
print("Start Testing")
test_loss = 0
total = 0
right = 0
with torch.no_grad():
    games_wins = np.load('Data\data_bits_normal_computerchess_wins_test.npy').astype(float)
    games_wins_crop = games_wins[np.random.choice(len(games_wins), size=50000, replace=False)]

    games_loss = np.load('Data\data_bits_normal_computerchess_loss_test.npy').astype(float)
    games_loss_crop = games_loss[np.random.choice(len(games_loss), size=50000, replace=False)]

    datasetTest = GamesDataset(games_wins_crop, games_loss_crop)
    dataLoaderTest = DataLoader(dataset=datasetTest, batch_size=64)

    for (pos1,pos2,res) in dataLoaderTest:
        
        pos1 = pos1.to(device)
        pos2 = pos2.to(device)
        res = res.to(device)

        _, encode1 = modelAE(pos1)
        _, encode2 = modelAE(pos2)

        input = torch.cat((encode1,encode2), 1)
        
        out = model(input)
        loss = criterion(out, res)

        pred = (out.cpu().detach().numpy() > .5).astype(int)
        corr = res.cpu().detach().numpy().astype(int)

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