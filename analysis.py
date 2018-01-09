import sys
sys.path.append('./mc_clustering')

from MC_Simulation import MC_Simulation
from analyse_norm import analyse_norm
import matplotlib.pyplot as plt
from joint_mass_vs_radius import joint_mass_vs_radius
from joint_mass_hist import joint_mass_hist
from joint_eccentricity_hist import joint_eccentricity_hist

print('\n         ANALYZING MINICLUSTERS         ')
print('----------------------------------------')

#----------finding the norm----------
print('\n1.) ANALYZING MC-NORMALISATION')

# analyse_norm(...)
# 1st argument: folder to search for simulations
#               -> last .m file of each simulation is chosen
# 2nd argument: folder to save results of cluster analysis
# 3rd argument: prefix to save normalisation plot and log-file

# 1st return value: list if initialized MC_Simulation classes (normalized with the combined norm!)
# 2nd return value: combined norm of all simulations

#----------
#sims, norm = analyse_norm('./data/test_sets', './results/summary_plots', './results/summary_plots/norm')
#----------

#----------analyse individual simulations----------
print('\n2.) ANALYZING INDIVIDUAL SIMULATIONS    \n')
den_th = [15]

# MC_Simulation.find_clusters(...)
# only argument: density thresgold
# creates a instance of MC_Cluster and appends it to the MC_Simulation.cluster_list
# dictionary
# the MC_Clusters class stores the mass, radii etc of all clusters in the simulation

#----------
#for sim in sims:
#    for th in den_th:
#        sim.find_clusters(th)
#        sim.cluster_list[th].plot_all()
#----------
        
#----------read data for previously analyzed clusters----------
print('3.) READING IN DATA FROM PREVIOUS SIMULATIONS\n')

# MC_Simulation constructor
# 1st argument: simulation input file
# 2nd argument: file the previous analysis was saved to (hdf5 file type, don't spell out file extension)
# available kewword arguments to the MC_Simulation Constructor:
# *'preexists' (False): set to true to indicate to read from an existing file
# *'min_samples' (20): customize sk-lear DBSCAB algorithm
# *'algorithm' ('kd_tree'): customize sk-lear DBSCAB algorithm
# *'n_jobs' (-1): customize sk-lear DBSCAB algorithm
# *'norm' (-1): if set to a positive value use this to normalize the energy density, otherwise use box average

#----------
sims = []
sim = MC_Simulation('./data/test_sets/L4N2_01/m/axion.m.00115', './results/summary_plots/L4N2_01', preexists=True)
sims.append(sim)
sim = MC_Simulation('./data/test_sets/L6N3_00/m/axion.m.00114', './results/summary_plots/L6N3_00', preexists=True)
sims.append(sim)
sim = MC_Simulation('./data/test_sets/L9N3_00/m/axion.m.00169', './results/summary_plots/L9N3_00', preexists=True)
sims.append(sim)
#----------

#----------joint analysis----------
print('\n4.) GENERATING JOINT PLOTS ')

# common to all functions below
# 1st argument: list of MC_Simulations to consider
# 2nd argument: density threshold. If the required value is not in a simulations cluster_list this simulation will be ignored
# 3rd argument: prefix for the output files
# output: *.pdf file containing the plot
#         *.txt log-file (lists all considered data sets)
#
# joint_mass_hist(...), joint_eccentricity_hist keyword arguments
# *'only_L' (0): if bigger than 0 only simulations of the given length are considered
# *'only_N' (0): if bigger than 0 only simulations with the given number of points are considered
# *'only_D' (0): if bigger than 0 only simulations with the given grid spacing are considered
#
# joint_mass_vs_radius(...) keyqord arguments
# *'devel' (False): if set to true each data set is given a different color, otherwise only different N/L combinations are distinguished

#----------
for th in den_th:
    joint_mass_hist(sims, th, './results/summary_plots/mass_hist')
    joint_eccentricity_hist(sims, th, './results/summary_plots/ecc_hist')
    joint_mass_vs_radius(sims, th, './results/summary_plots/mass_vs_rad_' ,devel=False)
#    joint_mass_hist(sims, th, './results/summary_plots/mass_hist_L4', only_L = 4)
#    joint_mass_hist(sims, th, './results/summary_plots/mass_hist_N2', only_N = 2048)
#    joint_mass_hist(sims, th, './results/summary_plots/mass_hist_D4-2', only_D = 4./2048.)

#----------
    
print(' ')
