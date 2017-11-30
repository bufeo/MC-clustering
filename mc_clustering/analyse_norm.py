import sys
import numpy as np
import matplotlib.pyplot as plt

from MC_Simulation import MC_Simulation
import matplotlib.pyplot as plt
from collect_sims import collect_sims

def analyse_norm(in_dir, out_dir, out_file):

    print('\n1.) ANALYZING MC-NORMALISATION         ')

    sim_list, out_list = collect_sims(in_dir, out_dir)
    
    sim_dat = {}
    sims = []
    out_txt = out_file + '.txt'
    with open(out_txt, 'w') as f:
        f.write('ANALYZING MC NORMALISATION\n\n')
        f.write('including the following files:\n')
        print('\nincluding following files:')

        for i in range(0,len(sim_list)):
            print(' -> %s'%(sim_list[i]))
            f.write(' -> %s\n'%(sim_list[i]))
            sim = MC_Simulation(sim_list[i], out_list[i])
            sims.append(sim)
            if (sim.sizeL, sim.res) in sim_dat.keys():
                sim_dat[(sim.sizeL, sim.res)].append(sim.norm)
            else:
                sim_dat[(sim.sizeL, sim.res)] = [sim.norm]

        print('\nobtaining norms:')
        f.write('\nnorms found for individual sets:\n')
        norms_per_set = []
        norms_per_sim = []
        for param in sim_dat.keys():
            
            mu = np.mean(sim_dat[param])
            sigm = np.std(sim_dat[param])

            print('L=%d, N=%d: norm = %f +- %f' %(param[0], param[1], mu, sigm))
            f.write('L=%d, N=%d: norm = %f +- %f\n' %(param[0], param[1], mu, sigm))
            norms_per_set.append([param, mu, sigm])
            norms_per_sim += sim_dat[param]

        norm = np.mean(norms_per_sim)
        sig= np.std(norms_per_sim)
        
        f.write('\ncombined result from all files: norm = %f +- %f' %(norm, sig))
        plot_norms_over_delta(norms_per_set, norm, sig, out_file)
                    
    return sims, norm

def plot_norms_over_delta(norm_list, norm, sig, out_file):

    out_name = out_file + '.pdf'
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # plot combined results
    plt.axhline(y=norm, color='g', linestyle='-')
    plt.axhspan(norm-sig, norm+sig, facecolor='g', alpha=0.2)
    
    # plot results for individual sets
    for set in norm_list:

        label = '$L= %1.1f$, $N= %d$' %(set[0][0],set[0][1])
        delta = set[0][0]/set[0][1]

        plt.errorbar(delta, set[1], yerr=set[2], xerr=None, fmt='o', label=label, ls=None, capsize=4)

    plt.ylabel('average density [$(f_a H_1/\\tau)^2$]')
    plt.xlabel('grid spacing [$H_1 R_1$]')
    legend = plt.legend(numpoints=1)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('white')

    plt.savefig(out_name)

    return

        
    
        
    


