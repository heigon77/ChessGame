f1 = open('Data/data_bits_normal.csv', 'r')
print("Start reading")
Lines = f1.readlines()
f1.close()
f2 = open('Data/data_bits_normal_np.csv', 'w')

total = len(Lines)
num = 0
for line in Lines:

    if num % 1000 == 0:
        print(num, num * 100 / total)

    line = line.replace(" ",",")
    f2.write(line)

    num += 1

f2.close()