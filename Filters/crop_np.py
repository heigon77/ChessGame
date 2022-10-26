import numpy as np

np.random.seed(42)

games = np.load("Data\data_bits_normal_not_capture_np_26.npy")

print(games.shape)
wins = []
loss = []
for game in games:
    if game[-1] == 1:
        wins.append(game[:773])
    else:
        loss.append(game[:773])
    
new_np_wins = np.array(wins)
new_np_loss = np.array(loss)

np.random.shuffle(new_np_wins)
print(new_np_wins.shape)
np.save("Data\data_bits_normal_wins_train_26.npy", new_np_wins[:int(len(new_np_wins)-50000)])
np.save("Data\data_bits_normal_wins_test_26.npy", new_np_wins[int(len(new_np_wins)-50000):])

np.random.shuffle(new_np_loss)
print(new_np_loss.shape)
np.save("Data\data_bits_normal_loss_train_26.npy", new_np_loss[:int(len(new_np_loss)-50000)])
np.save("Data\data_bits_normal_loss_test_26.npy", new_np_loss[int(len(new_np_loss)-50000):])

# new_np = games[:2100000]

# print(new_np_win)
# print("--------------------")
# print(new_np_loss)

# games_wins = np.load('Data\data_bits_normal_wins.npy')
# games_wins_crop = games_wins[np.random.choice(len(games_wins), size=20000, replace=False)]

# games_loss = np.load('Data\data_bits_normal_loss.npy')
# games_loss_crop = games_loss[np.random.choice(len(games_loss), size=20000, replace=False)]

# print(np.concatenate(games_wins_crop[1], games_loss_crop[1]))
