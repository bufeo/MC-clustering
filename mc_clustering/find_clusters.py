import MC_Simulation
import numpy as np
from sklearn.cluster import DBSCAN
import sys

def find_clusters(pos, Sim):

    # 1. cluster the original data set
    print 'clustering original data...',
    sys.stdout.flush()

    db = DBSCAN(eps=Sim.eps, min_samples=Sim.min_samples,
                algorithm=Sim.algorithm, n_jobs=Sim.n_jobs).fit(pos)
    labels = np.array(db.labels_)
    nmc1 = len(set(labels))
    print 'done'

    # 2. shift the data by n/2 and take mod(n)
    n = Sim.n
    nh = n//2
    pos2 = (pos + [nh,nh,nh])%n

    # 3. cluster the shifted data set
    print 'clustering shifted data...',
    sys.stdout.flush()
       
    db2 = DBSCAN(eps=Sim.eps, min_samples=Sim.min_samples,
                 algorithm=Sim.algorithm, n_jobs=Sim.n_jobs).fit(pos2)
    labels2 = np.array(db2.labels_)
    nmc2 = len(set(labels2))
    print 'done'
    
    return labels, labels2
