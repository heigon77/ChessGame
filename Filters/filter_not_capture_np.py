f1 = open('Data/data_bits_normal_not_capture_computerchess26.csv', 'r')
print("Start reading")
Lines = f1.readlines()
f1.close()
f2 = open('Data/data_bits_normal_not_capture_np_26.csv', 'w')

total = len(Lines)
num = 0
for line in Lines:

    if num % 1000 == 0:
        print(num, num * 100 / total)

    if "False" in line:
        line = line.replace(" ",",")
        line = line[:1547]
        f2.write(f"{line}\n")

    num += 1

f2.close()