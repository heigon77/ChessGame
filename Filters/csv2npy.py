import numpy as np

np.random.seed(42)

games = np.loadtxt("Data\data_bits_normal_not_capture_np_computerchess.csv", delimiter=",", dtype=float)

np.save("Data\data_bits_normal_not_capture_np_computerchess.npy", games)

