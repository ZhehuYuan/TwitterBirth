import numpy as np
from sklearn.cluster import KMeans

# This method must be given number of cluster

if __name__ == '__main__':
    file = open("us")
    data = []
    x = []
    dic = "abcdefghijklmnopqrstuvwxyz -_+-*/|\/.,<>?:;"
    user = [1, 1, 1]
    for line in file:
        print(line)
        x = input()
        if line[:4] == "Name":
            x = line[6:]
            if user == [1, 1, 1]:
                data.append(user)
            b = []
            for i in x:
                try:
                    if i in dic:
                        b.append(ord(i))
                except:
                    continue
            while len(b) < 10:
                b.append(0)
            user[0] = b
        if line[:3] == "Bio" and len(line) > 5:
            x = line[5:]
            for i in x:
                try:
                    if i in dic:
                        b.append(ord(i))
                except:
                    continue
            while len(b) < 20:
                b.append(0)
            user[1] = b
        if line[:11] == "Screen Name":
            x = line[13:]
            for i in x:
                try:
                    if i in dic:
                        b.append(ord(i))
                except:
                    continue
            while len(b) < 10:
                b.append(0)
            user[2] = b
    print(len(data))
    # km = KMeans(n_clusters=2)
    # label = km.fit_predict(data)
    # expenses = np.sum(km.cluster_centers_, axis=1)
    # # print(expenses)
    # CityCluster = [[], [], [], []]
    # for i in range(len(cityName)):
    #     CityCluster[label[i]].append(cityName[i])
    # for i in range(len(CityCluster)):
    #     print("Expenses:%.2f" % expenses[i])
    #     print(CityCluster[i])