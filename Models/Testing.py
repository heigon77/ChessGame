import numpy as np
import torch
from torch import nn
from Autoencoder import Autoencoder
from Siamese import Siamese, GamesDataset
from torch.utils.data import DataLoader

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
np.random.seed(42)

modelAE = Autoencoder()
checkpoint = torch.load("Models\checkpointNew.pth")

modelAE.load_state_dict(checkpoint['modelAE_state_dict'])
modelAE.to(device)
modelAE.eval()

model = Siamese()
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

criterion = nn.BCELoss()

test_loss = 0
total = 0
right = 0

print("BCELoss:",checkpoint['loss'])

with torch.no_grad():
    games_wins = np.load('Data\data_bits_normal_wins_test.npy').astype(float)
    games_wins_crop = games_wins[np.random.choice(len(games_wins), size=50000, replace=False)]

    games_loss = np.load('Data\data_bits_normal_loss_test.npy').astype(float)
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

        test_loss += loss

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