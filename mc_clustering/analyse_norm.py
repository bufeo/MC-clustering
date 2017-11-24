import sys
import numpy as np

from MC_Simulation import MC_Simulation
import matplotlib.pyplot as plt
from collect_sims import collect_sims

def analyse_norm(in_dir, out_dir, out_file):

    print('\n1.) ANALYZING MC-NORMALISATION         ')

    sim_list, out_list = collect_sims(in_dir, out_dir)
    
    sim_dat = {}
    sims = []
    
    print('\nincluding following files:')

    for i in range(0,len(sim_list)):
        print(' -> %s'%(sim_list[i]))
        sim = MC_Simulation(sim_list[i], out_list[i])
        sims.append(sim)
        if (sim.sizeL, sim.res) in sim_dat.keys():
            sim_dat[(sim.sizeL, sim.res)].append(sim.norm)
        else:
            sim_dat[(sim.sizeL, sim.res)] = [sim.norm]

    print('\nobtaining norms:')
    for param in sim_dat.keys():
        mu = np.mean(sim_dat[param])
        sigm = np.std(sim_dat[param])

        print('L=%d, N=%d: norm = %f +- %f' %(param[0], param[1], mu, sigm))

    norm = 0
    return sims, norm
