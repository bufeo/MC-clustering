import time
from MC_Clusters import MC_Clusters
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from analyse_norm import check_final_time

def joint_mass_vs_radius(sim_list, th, out_name, **kwargs):
    
    print('-> joint mass vs. radius plot for thereshold %1.1f' %(th))
    
    #1.) read kw-args
    devel = kwargs.pop('devel',False)
    r_type  = kwargs.pop('r_type', 2)  # which type of radius to consider
                                       # 1: half maximum radius
                                       # 2: mass weightd radius
                                       # 3: 90% radius

    #2.) initialise outputs & test at least one can be opened
    plot_filename = out_name + '.pdf'
    log_filename  = out_name + '.txt'
    date = time.localtime()

    with open(log_filename, 'w') as log_out:
        log_out.write('        log-file for mass vs. radius plots        \n')
        log_out.write('--------------------------------------------------\n')
        log_out.write('-> creation on %d/%d/%d at %d:%d\n' %(date.tm_mday, date.tm_mon, date.tm_year, date.tm_hour, date.tm_min))
        log_out.write('-> threshold %1.2f\n' %(th))
        log_out.write('-> plot file: %s\n' %(plot_filename))
        log_out.write('simulations used:\n')

    #3.) collect all sims with attributes
    mc_list = {}
    for sim in sim_list:
        if th in sim.cluster_list.keys():

            
            if not devel:
            # order simulations according to L and N
                if (sim.sizeL, sim.res) in mc_list.keys():
                    mc_list[(sim.sizeL, sim.res)].append(sim.cluster_list[th])
                else:
                    mc_list[(sim.sizeL, sim.res)] = [sim.cluster_list[th]]

            else:
            # consider each sim individually
                mc_list[sim.input_data] = [sim.cluster_list[th]]

    #4.) write all simulations included to the log file
    with open(log_filename, 'a') as log_out:
        for dset in mc_list.keys():
            for mc in mc_list[dset]:
                log_out.write('-> %s\n' %(mc.input_data))
    
    same, tmin, tmax = check_final_time(sim_list)
    if not same:
        with open(log_filename, 'a') as log_out:
            log_out.write('WARNING: not all data sets have the same final time:\n\n')
            log_out.write('%1.2f < z_final < %1.2f\n' %(tmin, tmax))
            
    #5.) initialize colors
    n_col = len(mc_list.keys())
    colors = [plt.cm.jet(each)
              for each in np.linspace(0, 1, n_col)]
    c_count = 0
        
    #6.) initialise and customize figure
    fig = plt.figure()
    ax = fig.add_subplot(111)

    #6.a) label according to radius choice
    if r_type == 1:
        r_string = 'Half maximum radius [$r/H_1 R_1$]'
    elif r_type == 2:
        r_string = 'Mass weighted radius [$r/H_1R_1$]'
    elif r_type == 3:
        r_string = 'Radius containing 90% of the total mass [$r/H_1R_1$]'
    else:
        print('choice of radius type not valid')
        return 0
    
    plt.yscale('log')
    plt.xscale('log')
    plt.ylabel(r_string)
    plt.xlabel('Mass [$M_1$]')
    plt.title('Mass vs. Radius for a Threshold of %1.1f' %(th))
       


    #7.) plot data sets
    for dset in mc_list.keys():
        
        #7.a) select correct label
        if not devel:
            label = '$L= %1.1f$, $N= %d$' %(dset[0],dset[1])
        else:
            label = dset
            
        for mc in mc_list[dset]:

            #7.b) select correct radius type
            if r_type == 1:
                radius = mc.r_half_max
            elif r_type == 2:
                radius = mc.r_mass_weighted
            elif r_type == 3:
                radius = mc.r_90pc

            #7.c) get simulation properties
            delta = mc.sizeL/mc.n
            unitmass = (delta)**3

            #7.d) plot data
            plt.scatter(unitmass*mc.mass,delta*radius,
                        c=colors[c_count], lw=0, rasterized=True, label=label,
                        s=5)
            
            c_count += 1

    #9.)finalize and save
    legend = plt.legend(numpoints=1)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_edgecolor('white')

    plt.savefig(plot_filename)

    #10.) write information to log file and promt
    with open(log_filename, 'a') as log_out:
        log_out.write('\n...plotting finished succesfully')

    print('   saved to: %s' %(plot_filename))






    
