import numpy as np
import sklearn.cluster as skc
from sklearn import metrics
import matplotlib.pyplot as plt

# Don't need to be given number of cluster

onlinetimes = {}
with open("filename", encoding="utf8") as f:
    for line in f:
        info_list = line.strip().split(',')
        mac = info_list[2]
        onlinetime = int(info_list[6])
        starttime = int(info_list[4].split(' ')[1].split(':')[0])
        onlinetimes[mac] = (starttime, onlinetime)
real_X = np.array([onlinetimes[key] for key in onlinetimes]).reshape((-1, 2))
X = real_X[:, 0:1]

db = skc.DBSCAN(eps=0.01, min_samples=20).fit(X)
labels = db.labels_

raito = len(labels[labels[:] == -1]) / len(labels)
print('Noise raito:', format(raito, '.2%'))

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print('Estimated number of clusters: %d' % n_clusters_)
print("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

for i in range(n_clusters_):
    print('Cluster ', i, ':')
    print(list(X[labels == i].flatten()))

plt.hist(X, 24)
plt.show()