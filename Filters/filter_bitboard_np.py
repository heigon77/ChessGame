f1 = open('Data\data_bits_normal.csv', 'r')
Lines = f1.readlines()
f1.close()
f2 = open('Data\data_bits_normal_np.csv', 'w')

for line in Lines:
    line = line.replace(" ",",")
    f2.write(line)

f2.close()