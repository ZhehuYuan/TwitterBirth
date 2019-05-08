import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
# This method must be given number of cluster

if __name__ == '__main__':
    data = []
    user = [1, 1, 1]
    name = []
    ix = 0
    male = []
    file = open("Males", errors="ignore")
    # for unreadable symbol
    for line in file:
        # ignore lines with no data
        if line == "\n":
            continue
        ix += 1
        # first line of data is some strange sample
        if ix == 1:
            continue
        # use screen name as identity of a user
        if ix % 3 == 2:
            # add identity to male labeled identity
            male.append(line)
            # mix identity with unlabeled identity
            name.append(line)
        # **** pick the data you want to train, don't uncommon the text inside []
        # if ix % 3 == 2: # [uncommon this line to train screen name as data]
        # if ix % 3 == 1: # [uncommon this line to train name as data]
        # if ix % 3 == 3: # [uncommon this line to train screen bios as data]
            x = []
            for i in line:
                # use ascii code to read string
                x.append(ord(i))

            while len(x) < 10: # **** change the "10" here to 20 if you want to train bio as data
                # fix length for short input, length of bios is 20, length of name and screen name are 10
                x.append(0)
            # mix training data with unlabeled training data
            data.append(x[:10])
    # print out len(data) collected
    print("Num of male: "+str(len(male)))
    print("Num of male: "+str(len(name)))
    print("Num of data till now: "+str(len(data)))
    # only want 100 labeled male's data
    male = male[:100]

    # same as reading Males
    ix = 0
    female = []
    file = open("Females", errors="ignore")
    for line in file:
        if line=="\n":
            continue
        ix += 1
        if ix == 1:
            continue
        if ix % 3 == 2:
            female.append(line)
            name.append(line)
        # **** pick the data you want to train, don't uncommon the text inside []
        # if ix % 3 == 2: # [uncommon this line to train screen name as data]
        # if ix % 3 == 1: # [uncommon this line to train name as data]
        # if ix % 3 == 3: # [uncommon this line to train screen bios as data]
            x = []
            for i in line:
                x.append(ord(i))
            while len(x) < 10: # **** change the "10" here to 20 if you want to train bio as data
                x.append(0)
            data.append(x[:10])
    print("Num of female: "+str(len(female)))
    print("Num of male and female: "+str(len(name)))
    print("Num of data till now: "+str(len(data)))
    female = female[:100]

    # read unlabeled data
    file = open("us", errors="ignore")
    # bool value, to avoid repeat data with supervised data
    repeat = 1
    for line in file:
        if line[:4] == "Name":
            # read Name
            x = line[6:]
            b = []
            for i in x:
                try:
                    b.append(ord(i))
                except:
                    continue
            while len(b) < 10:
                b.append(0)
            user[0] = b[:10]
            # **** uncommon next 2 lines if you want to collect Name as training data
            # if repeat == 0:
            #     data.append(user[0])
        elif line[:3] == "Bio":
            # read Bio
            x = line[3:]
            b = []
            for i in x:
                try:
                    b.append(ord(i))
                except:
                    continue
            while len(b) < 20:
                b.append(0)
            user[1] = b[:20]
            # **** uncommon next 2 lines if you want to collect Bios as training data
            # if repeat == 0:
            #     data.append(user[1])
        elif line[:11] == "Screen Name":
            # read Screen Name
            x = line[13:]
            b = []
            for i in x:
                try:
                    b.append(ord(i))
                except:
                    continue
            while len(b) < 10:
                b.append(0)
            user[2] = b[:10]
            if not (x in name):
                # use screen name as identity of user
                name.append(x)
                repeat = 0
            else:
                repeat = 1
            # **** uncommon next 2 lines if you want to collect Screen Name as training data
            # if repeat == 0:
            #     data.append(user[2])
        else:
            continue
    # print the data collected
    print("Num of name totally: "+str(len(name)))
    print("Num of data totally: "+str(len(data)))
    # use PCA to decrease the size of data to 1 dem
    pca = PCA(n_components=1)
    data = pca.fit_transform(np.array(data))
    # use unsupervised learning to get 2 cluster
    km = KMeans(n_clusters=2)
    # train user's data into 2 cluster
    label = km.fit_predict(data)
    expenses = np.sum(km.cluster_centers_, axis=1)
    Cluster = [[], []]
    # separate identity of users to 2 clusters
    for i in range(len(data)):
        Cluster[label[i]].append(name[i])
    m1 = 0
    m2 = 0
    f1 = 0
    f2 = 0
    m = 0
    f = 0
    # check how much of labeled male and female in each cluster,
    # in order to determine the gender of each cluster
    for i in male:
        if i in Cluster[0]:
            m1 += 1
        elif i in Cluster[1]:
            m2 += 1
        if i in name:
            m += 1
    for i in female:
        if i in Cluster[0]:
            f1 += 1
        elif i in Cluster[1]:
            f2 += 1
        if i in name:
            f += 1
    # print out result
    print("male in Cluster0: "+str(m1), "female in Cluster0: "+str(f1), "male in cluster1: "+str(m2), "female in cluster1: "+str(f2))
    print("Cluster0: "+str(len(Cluster[0])), "Cluster1: "+str(len(Cluster[1])))
