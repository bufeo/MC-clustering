import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

from random import randint
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.distance import pdist

import time
import sys
import h5py

from math import pow
from math import ceil

#TO DO
#speed up the loop over data -> using cython?
#do periodic boundaries really work??
#then start processing the data!

print('--------------------------------------------------')
print('Finding Minicluster Progenitors')
print('--------------------------------------------------')
print('periodic boundary conditions are accounted for by subsequent gluing\n')

start_g = time.time()

#parameters relating to the provided data
data_file = '../data/axion.00059'
output_file = './results/example.txt'
if len(sys.argv)==3:
    data_file = sys.argv[1]
    output_file = sys.argv[2]

print('input data:\t%s\noutpu data:\t%s\n' %(data_file, output_file))

#parameters for DBSCAN
eps=5
min_samples=20
algorithm='kd_tree'
n_jobs=-1

#further parameter  
dens_th = 5

print('the clustering parameters are:')
print('eps:\t\t %d\nmin_samples:\t %d\nalgorithm:\t %s\nn_jobs:\t\t %d\nthereshold\t%1.1f\n' %(eps,min_samples,algorithm,n_jobs,float(dens_th)))

#reading in the data
print('reading data...')
start=time.time()

pos = []   #position of every overdense point
dens = []  #value of every overdense point

file = h5py.File(data_file, 'r')
data = file['m'].value
file.close()

end=time.time()
print('gettin the array from file took %1.3f s' %(end-start))

start=time.time()
n_ax = int(pow(len(data),1./3.)+10**-5)

for i in xrange (0, n_ax):
    for j in xrange (0, n_ax):
        for k in xrange (0, n_ax):

            if (data[k+ n_ax*j+ n_ax*n_ax*i] >= dens_th):
                pos.append([i,j,k])
                dens.append(data[k+ n_ax*j+ n_ax*n_ax*i])

pos = np.array(pos)
end=time.time()
n_points = len(dens)

print('preparing data took %1.3f min' %((end-start)/60.))
print('array size is %d x %d x %d' %(n_ax,n_ax,n_ax))
print('#of points above threshold: %d (%1.2f pc of total points)\n' %(n_points, n_points*100./n_ax**3))

print('starting the clustering...')
start = time.time()
db = DBSCAN(eps=eps, min_samples=min_samples, algorithm=algorithm, n_jobs=n_jobs).fit(pos)
end = time.time()

print('simple euclidean took %1.3f min' %((end-start)/60.))

labels = list(db.labels_)

#redoing the clustering on the boundaries
pos_b = []
labels_old = []
start = time.time()

for axis in xrange(0,3):
    for i in range (0, n_points):
        if (pos[i][axis] < eps):
            pos_b.append(pos[i])
            labels_old.append(i)
        elif (pos[i][axis] > n_ax-eps-1):
            if (axis==0):
                pos_b.append([pos[i][0]-n_ax, pos[i][1], pos[i][2]])
            elif(axis==1):
                pos_b.append([pos[i][0], pos[i][1]-n_ax, pos[i][2]])
            elif(axis==2):
                pos_b.append([pos[i][0], pos[i][1], pos[i][2]-n_ax])
            labels_old.append(i)
        
if (len(pos_b)>1):      
    db_b = DBSCAN(eps=eps, min_samples=min_samples, algorithm=algorithm, n_jobs=n_jobs).fit(pos_b)

    labels_b = np.array(db_b.labels_)
    labels_old = np.array(labels_old)

    #now glue the thing together
    #loop over new clusters
    for i in set(labels_b):

        if (i!=-1):
            mask_old = (labels_b == i)
            values_old = set(labels_old[mask_old]) 

            #the algorithm cant assign previously noisy points to a cluster
            #just joins clusters
            if -1 in values_old:
                values_old.remove(-1)

                new_index = min(values_old)
                for x in xrange(0, len(labels)):
                    for index in values_old:
                        if (labels[x]==index):
                            labels[x]=new_index

end=time.time()
print('gluing the boundaries took %1.2f s\n' %(end-start) )
    

#print some statistics
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = labels.count(-1)

print('RESULTS:')
print('Number of clusters found:\t %d' %n_clusters)
print('Number of noisy points:\t\t %d\n' %n_noise )


#plotting Data
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim3d(0, n_ax)
ax.set_ylim3d(0, n_ax)
ax.set_zlim3d(0, n_ax)


unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

for k, col in zip(unique_labels, colors):
    if (k>-1):

        class_member_mask = (labels == k)
        xyz = pos[class_member_mask] #list of coordinates of all points in one cluster

        #plot projection on x-y plane
        #plt.plot(xyz[:, 0], xyz[:, 1], 'o', markerfacecolor=col, markersize=6)

        #3D plot
        if ( np.size(xyz) > 3*500 ):
            ax.scatter(xyz[:,0], xyz[:,1], xyz[:,2], c=col, s=6, lw=0)
        
end_g = time.time()
print('total runtime was %1.1f min' %((end_g-start_g)/60.))

plt.show()

print('--------------------------------------------------')
print('--------------------------------------------------')



exit()
