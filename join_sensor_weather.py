# interpolate data

import pandas as pd
import numpy as np
import csv

with open("file1.csv", "rt") as file1:
    data1 = []
    rdr = csv.reader(file1)
    for row in rdr:
        data1.append((row[0], row[2]))

with open("file2.csv", "rt") as file1:
    data2 = []
    rdr = csv.reader(file1)
    for row in rdr:
        data2.append((row[0], row[5]))

x1, y1 = zip(*data1)
x2, y2 = zip(*data2)


def dates_to_array(data):
    x_hdr = data[0]
    x = list(map(lambda s: str(pd.to_datetime(s)), data[1:]))
    x = np.array(x, dtype=np.datetime64)
    return x_hdr, x


x1_hdr, x1 = dates_to_array(x1)
y1_hdr = y1[0]
y1 = np.array(list(map(int, y1[1:])))

x2_hdr, x2 = dates_to_array(x2)
y2_hdr = y2[0]
y2 = np.array(list(map(int, y2[1:])))

import matplotlib.pyplot as plt

plt.plot(x1, y1)
plt.plot(x2, y2)
plt.xticks(rotation="vertical")
plt.show()