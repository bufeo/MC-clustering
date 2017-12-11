import sys
sys.path.append('./mc_clustering')

from MC_Simulation import MC_Simulation
from analyse_norm import analyse_norm
import matplotlib.pyplot as plt
from joint_mass_vs_radius import joint_mass_vs_radius

print('\n         ANALYZING MINICLUSTERS         ')
print('----------------------------------------')

#----------finding the norm----------
print('\n1.) ANALYZING MC-NORMALISATION         ')
sims, norm = analyse_norm('./data/test_sets', './results/summary_plots', './results/summary_plots/summary')

#----------analyse individual simulations----------
print('\n2.) ANALYZING INDIVIDUAL SIMULATIONS    \n')
den_th = [15]
for sim in sims:
    for th in den_th:

        sim.find_clusters(th)
#       sim.cluster_list[th].plot_all()



#----------joint analysis----------
print('\n3.) GENERATING JOINT PLOTS             ')
for th in den_th:
    joint_mass_vs_radius(sims, th, './results/summary_plots/mass_vs_rad_' ,devel=False)

