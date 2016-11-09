import matplotlib.pyplot as plt

def calpro(filename):
    fo = open(filename + ".txt", "r")
    data = fo.readlines()
    total = 0
    list = []
    for line in data:
        line = line.split()
        line = line[len(line) - 1]
        number = line.split(')')[0]
        list.append(int(number, 0))
        total = total + int(number, 0)

    i = 0
    result = []
    x = []
    y = []
    for tf in list:
        x.append(i + 1)
        y.append(list[i] / float(total))
        i = i + 1
    result.append(x)
    result.append(y)
    return result

result1 = calpro('task3-1a')
plt.figure(1)
plt.plot(result1[0][0:400], result1[1][0:400], 'b-', markersize=20)
plt.xlabel("rank of the term")
plt.ylabel("probability")
plt.title("Zipfian curves for n = 1")

result2 = calpro('task3-2a')
plt.figure(2)
plt.plot(result2[0][0:500], result2[1][0:500], 'b-', markersize=20)
plt.xlabel("rank of the term")
plt.ylabel("probability")
plt.title("Zipfian curves for n = 2")

result3 = calpro('task3-1a')
plt.figure(3)
plt.plot(result3[0][0:400], result3[1][0:400], 'b-', markersize=20)
plt.xlabel("rank of the term")
plt.ylabel("probability")
plt.title("Zipfian curves for n = 3")
plt.show()

