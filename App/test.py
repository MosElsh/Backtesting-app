file = open("SPX Ticker List.csv", "r")
for line in file:
    line = line.replace("\n", "")
    print(line)

file.close()