import sys
sys.path.append('./mc_clustering')

from MC_Simulation import MC_Simulation
from analyse_norm import analyse_norm
import matplotlib.pyplot as plt
from joint_mass_vs_radius import joint_mass_vs_radius
from joint_mass_hist import joint_mass_hist

print('\n         ANALYZING MINICLUSTERS         ')
print('----------------------------------------')

#----------finding the norm----------
#
# analyse_norm(...)
# 1st argument: folder to search for simulations
#               -> last .m file of each simulation is chosen
# 2nd argument: folder to save results of cluster analysis
# 3rd argument: prefix to save normalisation plot and log-file

# 1st return value: list if initialized simulation classes
# 2nd return value: combined norm of all simulations

print('\n1.) ANALYZING MC-NORMALISATION')
sims, norm = analyse_norm('./data/test_sets', './results/summary_plots', './results/summary_plots/norm')

#----------analyse individual simulations----------
#
# MC_Simulation.find_clusters(...)
# only argument: density thresgold
# creates a instance of MC_Cluster and appends it to the MC_Simulation.cluster_list
# dictionary
# the MC_Clusters class sores the mass, radii etc of all clusters in the simulation

print('\n2.) ANALYZING INDIVIDUAL SIMULATIONS    \n')
den_th = [15]
for sim in sims:
    for th in den_th:

        sim.find_clusters(th)
#       sim.cluster_list[th].plot_all()



#----------joint analysis----------
print('\n3.) GENERATING JOINT PLOTS             ')
for th in den_th:
    joint_mass_hist(sims, th, './results/summary_plots/mass_hist')
    joint_mass_hist(sims, th, './results/summary_plots/mass_hist_L4', only_L = 4)
    joint_mass_hist(sims, th, './results/summary_plots/mass_hist_N2', only_N = 2)
    joint_mass_vs_radius(sims, th, './results/summary_plots/mass_vs_rad_' ,devel=False)
    
