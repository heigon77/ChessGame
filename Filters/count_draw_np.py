f1 = open('Data\data_bits_drawed.csv', 'r')
Lines = f1.readlines()
f1.close()
f2 = open('Data\data_bits_drawed_np.csv', 'w')

for line in Lines:
    line = line.replace(" ",",")
    f2.write(line)

f2.close()