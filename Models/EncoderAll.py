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
games = np.load("Data\data_bits_normal_not_capture_np.npy")

datasetTrain = GamesDatasetTrain(games[:int(len(games))])
dataLoaderTrain = DataLoader(dataset=datasetTrain)

model = Autoencoder()
checkpointDBN = torch.load("Models\checkpointDBN.pth")

model.load_state_dict(checkpointDBN['model_state_dict'])
model.to(device)
epoch_ini = checkpointDBN['epoch']
epoch_ini += 1
model.eval()
dataset = []

print("Start Evaluating")

num = 0

with torch.no_grad():
    for (pos,label) in dataLoaderTrain:
        num += 1

        if(num%1000 == 0):
            print(num, num * 100 / len(dataLoaderTrain.dataset))
        pos = pos.to(device)

        recon, code = model(pos)

        code_np = code.cpu().detach().numpy()[0]
        label_np = label.detach().numpy()[0]
        dataset.append(np.concatenate((code_np,label_np)))



print("Finish Training")

data_np = np.array(dataset)
np.save("Data\data_bits_normal_encoded_all_not_capture.npy", data_np)

runningTime = (time.time() - start_time)
print(f"--- {runningTime:2f}s seconds ---")