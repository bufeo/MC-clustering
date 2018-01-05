import time
from MC_Clusters import MC_Clusters
import numpy as np
import matplotlib.pyplot as plt
from analyse_norm import check_final_time

def joint_mass_hist(sim_list, th, out_name, **kwargs):

    print('-> joint mass histogramm for thereshold %1.1f' %(th))

    #1.) read keyword arguments & check
    lonly = kwargs.pop('only_L', 0)
    nonly = kwargs.pop('only_N', 0)
    donly = kwargs.pop('only_D', 0)

    if lonly+nonly+donly > max([lonly, donly, nonly]):
        print('\nERROR in computing the joint mass histogramm')
        print('too many constraints on simulation parameters')
        print('you can specify at most one of the following options:')
        print('only_L, only_N, only_D\n')
        return
    
    elif lonly<0 or nonly<0 or donly<0:
        print('\nERROR in computing the joint mass histogramm')
        print('the following optional argumnts can only be positiv:')
        print('only_L, only_N, only_D\n')
        return
        
    #2.) initialise outputs & test if the log-file can be opened
    plot_filename = out_name + '.pdf'
    log_filename  = out_name + '.txt'
    date = time.localtime()

    with open(log_filename, 'w') as log_out:
        log_out.write('           log-file for mass histogramm           \n')
        log_out.write('--------------------------------------------------\n')
        log_out.write('-> created on %d/%d/%d at %d:%d\n' %(date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour, date.tm_min))
        log_out.write('-> threshold %1.2f\n' %(th))
        log_out.write('-> plot file: %s\n' %(plot_filename))

        if lonly>0:
            log_out.write('\n only considering simulations with L = %1.2f\n' %(lonly))
        elif nonly>0:
            log_out.write('\n only considering simulations with N = %d\n' %(nonly))
        elif donly>0:
            log_out.write('\n only considering simulations with delta = %1.5f\n' %(donly))

        log_out.write('\nsimulations used:\n')



    #3.) collect minicluster masses of all simulations
    mc_masses = np.array([])
    n_sims = 0
    for sim in sim_list:
        if th in sim.cluster_list.keys():

            # consider conditions on N/L/delta
            incl = True
            if lonly>0 and sim.sizeL != lonly:
                incl = False
            elif nonly>0 and sim.n != lonly:
                incl = False
            elif donly>0 and (sim.sizeL/sim.n) != donly:
                incl = False

            if incl:
                
                # compute cluster mass normalized to M_1
                unitmass = (sim.sizeL/sim.n)**3
                mmcs = sim.cluster_list[th].mass*unitmass
                mc_masses = np.append(mc_masses, mmcs)
                n_sims += 1

                # write simualtion to log file
                with open(log_filename, 'a') as log_out:
                   log_out.write('-> %s\n' %(sim.input_data))

    #3.) write additional information to the log file
    with open(log_filename, 'a') as log_out:
        log_out.write('\n=> total number of simulations: %d\n' %(n_sims))
        log_out.write('=> total number of clusters: %d' %(len(mc_masses)))
        log_out.write('\n')

    #4.) check that all simulations have the same final time
    same, tmin, tmax = check_final_time(sim_list)
    if not same:
        with open(log_filename, 'a') as log_out:
            log_out.write('WARNING: not all data sets have the same final time:\n\n')
            log_out.write('%1.2f < z_final < %1.2f\n' %(tmin, tmax))
                
    #5.) to show the fractional distribution instead of apsolute number
    #    introduce a weight. This changes only the labels in the y-axis.
    weights = np.ones_like(mc_masses)/float(len(mc_masses))

    #6.) customize the plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xscale('log')
    plt.xlabel('Mass [$M_1$]')
    plt.title('Distribution of MC masses for a Threshold of %1.1f' %(th))

    #7.) plot and save
    plt.hist(mc_masses,bins=np.logspace(-5,1,20), lw=0,weights=weights)
    plt.savefig(plot_filename)
    
    #8.) print additional
    with open(log_filename, 'a') as log_out:
        log_out.write('\n...plotting finished succesfully')

    print('   saved to: %s' %(plot_filename))
