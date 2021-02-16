import csv
import math
import numpy as np


def load_data(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dct = []
        tst = []
        for row in reader:
            tst2 = []
            a = row['Province/State']
            b = row['Country/Region']
            if a:
                c = a + ", " + b
            else:
                c = b
            x = {'Region': c}

            for key in row:
                if key != 'Province/State' and key != 'Country/Region' and key != 'Lat' and key != 'Long':
                    x[key] = int(row[key])
                    tst2.append(x[key])
            dct.append(x)
            tst.append(tst2)

        return tst


def calculate_x_y(time_series):
    i = len(time_series) - 1
    n = time_series[i]
    t = 0  # track days passed
    y = 0
    x = 0
    c = 0
    time_series.reverse()
    for item in time_series:  # find x value
        t += 1
        z = item
        if n / 10 >= z >= c:
            c = z
            x = t
            break
    t = 0
    for item in time_series:  # find y value
        t += 1
        if item <= int(n / 100):
            y = t
            break
    y = y - x
    return [x - 1, y]


def findmin(c):
    m = {'val': float('inf'), 'row': 244, 'col': 244}

    for col in range(len(c[0]) - 1):
        col += 1

        for row in range(len(c)):

            v = c[row][col]
            if not v and v != 0:
                v = float('inf')
            if v <= m['val']:
                # values for tiebreaking
                newrow, newcol, oldrow, oldcol = 0, 0, 0, 0
                if c[row][0] < c[col][0]:
                    newrow = c[row][0]
                    newcol = c[col][0]
                else:
                    newrow = c[col][0]
                    newcol = c[row][0]
                if c[m['row']][0] < c[m['col'] - 1][0]:
                    oldcol = c[m['col'] - 1][0]
                    oldrow = c[m['row']][0]
                else:
                    oldcol = c[m['row']][0]
                    oldrow = c[m['col'] - 1][0]
                if v == m['val']:
                    if newrow < oldrow:
                        m = {'val': v, 'row': row, 'col': col}
                    elif newcol < oldcol and newrow == oldrow:
                        m = {'val': v, 'row': row, 'col': col}
                else:
                    m = {'val': v, 'row': row, 'col': col}

    return m['val'], m['col'] - 1, m['row'], c[m['col'] - 1][0], c[m['row']][0]


def getmatrix(dataset):
    c = []

    x = 0
    l = len(dataset)

    for item in dataset:

        n = 0
        v = [x]
        while n < l:
            if n >= x:
                v.append(None)
            else:
                val1 = math.pow((item[0] - dataset[n][0]), 2)

                val2 = math.pow((item[1] - dataset[n][1]), 2)
                v.append(math.sqrt(val1 + val2))

            n += 1
        c.append(v)
        x += 1
    return c


def getgroup(w, l, col):  # returns all group members for any cluster
    group = []

    if l <= col < 2 * l:
        group = group + (getgroup(w, l, w[col - l][0]))
        group = group + (getgroup(w, l, w[col - l][1]))
    else:
        group = group + [col]

    return group


def hac(dataset):
    set1 = []

    for vec in dataset:

        n = calculate_x_y(vec)
        if n[0] > 0 and n[1] >= 0:  # check for NaN
            set1.append(n)

    x = 0
    l = len(set1)
    c = []
    for item in set1:  # setup distance matrix

        n = 0
        v = [x]
        while n < l:
            if n >= x:
                v.append(None)
            else:
                val1 = math.pow((item[0] - set1[n][0]), 2)

                val2 = math.pow((item[1] - set1[n][1]), 2)
                v.append(math.sqrt(val1 + val2))

            n += 1
        c.append(v)
        x += 1

    i = 0
    w = []
    l = len(c)
    while i < l - 1:
        group = []
        min, lowcol, lowrow, newcol, newrow = findmin(c)
        group = group + getgroup(w, l, newcol)
        group = group + getgroup(w, l, newrow)
        group = sorted(list(dict.fromkeys(group)))

        for n in range(len(group)):
            if n + 1 < len(group):
                for d in range(len(group) - 1):
                    c[group[n + 1]][group[d] + 1] = float('inf')

            c[group[n]][0] = i + l

        i += 1
        if newcol < newrow:
            z = [newcol, newrow, min, len(group)]
        else:
            z = [newrow, newcol, min, len(group)]
        w.append(z)

    return np.asarray(w)


if __name__ == "__main__":
    dataset = load_data('time_series_covid19_confirmed_global.csv')
    w = hac(dataset)
    print(w)
