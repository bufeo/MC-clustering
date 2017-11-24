import sys
sys.path.append('./mc_clustering')

from MC_Simulation import MC_Simulation
from analyse_norm import analyse_norm
import matplotlib.pyplot as plt

print('\n         ANALYZING MINICLUSTERS         ')
print('----------------------------------------')

#----------finding the norm----------
sims, norm = analyse_norm('./data', './results/test_norm', './results/test_norm/summary')

#----------the analyse the clusters----------
#den_th = [5, 10, 15]
#for i in sim_list:
#    for th in den_th:

#        sim[i].find_clusters(th, norm=norm)
#        sim[i].cluster_list[th].plot_all()


