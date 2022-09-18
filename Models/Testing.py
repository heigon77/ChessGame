import numpy as np
import torch
from torch import nn
from Autoencoder import Autoencoder, GamesDatasetTest, GamesDatasetTrain
from torch.utils.data import DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
np.random.seed(42)

print("Loading Model")
model = Autoencoder()
model.load_state_dict(torch.load("Models\Autoencoder.pth"))
model.to(device)

criterion = nn.MSELoss()

print("Loading Data")
games = np.load('Data\data_bits_normal.npy')
np.random.shuffle(games)

datasetTrain = GamesDatasetTrain(games[:int(len(games)*.8)])
dataLoaderTrain = DataLoader(dataset=datasetTrain, batch_size=256)

datasetTest = GamesDatasetTest(games[int(len(games)*.8):])
dataLoaderTest = DataLoader(dataset=datasetTest, batch_size=256)

print(f"Train: {len(dataLoaderTrain.dataset)}")
print(f"Test: {len(dataLoaderTest.dataset)}")

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