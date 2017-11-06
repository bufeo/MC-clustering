import sys
sys.path.append('./mc_clustering')

from MC_Simulation import MC_Simulation
import matplotlib.pyplot as plt

print('\n         ANALYZING MINICLUSTERS         ')
print('----------------------------------------')

th_list = [5, 7, 10]

mc1 = MC_Simulation('./data/density_maps/L=2, 1024-_128(WKB)/axion.r.00076',
                   './results/test/L2-00076')

mc2 = MC_Simulation('./data/density_maps/L=3, 1536 -_ 256(WKB)/axion.r.00039',
                   './results/test/L3-00039')

mc3 = MC_Simulation('./data/density_maps/L=4, 1024-_256(WKB)/axion.r.00076',
                   './results/test/L4-00076')


mcs = [mc1, mc2, mc3]

#mcs = [mc1]
#th_list = [7]

for mc in mcs:
    for th in th_list:
        mc.find_clusters(th)
        mc.cluster_list[th].plot_all()


