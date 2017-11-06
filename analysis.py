import sys
sys.path.append('./mc_clustering')

from MC_Simulation import MC_Simulation
import matplotlib.pyplot as plt

print('\n         ANALYZING MINICLUSTERS         ')
print('----------------------------------------')

mc = MC_Simulation('./data/density_maps/L=3, 1536 -_ 256(WKB)/axion.r.00038',
                   './results/test/test1')
mc.find_clusters(5)
mc.cluster_list[5].plot_all()

mc.find_clusters(7.5)
mc.cluster_list[7.5].plot_all()

mc.find_clusters(9)
mc.cluster_list[9].plot_all()

