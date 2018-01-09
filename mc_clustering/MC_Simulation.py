import csv
import h5py
import numpy as np

from MC_Clusters import MC_Clusters
from find_sim_properties import find_norm
from find_sim_properties import find_n

class MC_Simulation:
    """Class to hold all information on one simulation"""

    ##############################
    # 1. Constructor
    ##############################
    def __init__(self, input_data, output_prefix, **kwargs):

        # 1.a) initialize arguments
        self.input_data = input_data
        self.output_prefix = output_prefix
        self.output_file = output_prefix + '.hdf5'
        self.eps = kwargs.pop('eps',2)
        self.min_samples = kwargs.pop('min_samples',20)
        self.algorithm = kwargs.pop('algorithm','kd_tree')
        self.n_jobs = kwargs.pop('n_jobs',-1)
        self.norm = kwargs.pop('norm',-1.)
        self.preexists = kwargs.pop('preexists', False)
        
        # 1.b) initialize variables holding the analysis
        self.cluster_list = dict()

        # 1.c) get information about the simulation
        #      and test if the input file can be opend
        with h5py.File(input_data, 'r') as input:
            self.sizeL = input.attrs[u'Physical size']
            self.zi = input.attrs[u'zInitial']
            self.zf = input.attrs[u'zFinal']
            self.zc = input.attrs[u'z']
            try:
                self.llambda = input.attrs[u'Lambda']
            except:
                self.llambda = -1
            try:
                self.nQCD = input.attrs[u'nQcd']
            except:
                self.nQCD = -1
            self.res = input.attrs[u'Size']
        self.n = find_n(self)
        self.n3 = self.n*self.n*self.n
        self.norm = find_norm(self)  #needs to be calles after n3 is defined  
            
        # 1.d) if there is no pre-existing output file:
        #      create output file & write information abou simulation
        #      (an existing file of the same name will be erased)
        if self.preexists == False:

            with h5py.File(self.output_file, 'w') as out_writer:
                out_writer.attrs['simulation_file'] = self.input_data      

        # 1.c) if there is a pre-existing output file:
        #      check it refers to the correct data file
        #      and read in all analysis from it
        else:
            with h5py.File(self.output_file, 'r') as out_reader:
                ifile = out_reader.attrs[u'simulation_file']
         
                # check the input file is correct
                if ifile != self.input_data:
                    print('\nERROR in reading data from a previous analysis:')
                    print('File names given as argument and read from data not matching!')
                    print('Aborting computation.\n')
                    exit()

                #loop over all thresholds saved in the file
                for th_grp in out_reader:

                    grp = out_reader[th_grp]
                    # call the constructor to get all basic information
                    thereshold = grp.attrs['threshold']
                    mc = MC_Clusters(thereshold, self, preexists=True)

                    # assign data read from file
                    n_clusters             = grp.attrs['n_clusters']
                    mc.norm                = grp.attrs[u'norm']
                    mc.n_points            = grp['n_points'].value
                    mc.mass                = grp['mass'].value
                    mc.r_half_max          = grp['r_half_max'].value
                    mc.r_mass_weighted     = grp['r_mass_weighted'].value
                    mc.r_90pc              = grp['r_90pc'].value
                    mc.momentum_of_inertia = grp['momentum_of_inertia'].value
                  
                    # append to the cluster list
                    self.cluster_list[thereshold] = mc
                    print('-> data file: %s, simulation file: %s, threshold %1.2f' %(ifile ,self.output_file, float(thereshold)))

                # 1.d) make sure all clusters have the same normalization
                #      and assign it to the simulation norm
                norms = [self.cluster_list[th].norm for th in self.cluster_list.keys()]
                nmin = min(norms)
                nmax = max(norms)
                if nmin == nmax:
                    self.norm = nmin
                else:
                    self.norm = -1
                    print('\nWARNING: not all clusters in this set use the same threshold.')
                    print('           %1.2f < norm < %1.2f\n' %(nmin, nmax))
                
    ##############################
    # 2. cluster properties for certain thereshold
    ##############################
    def find_clusters (self,thereshold):

        print('analyzing file %s for threshold %1.1f' %(self.input_data, thereshold))

        # 2.a) create an instance of the MC_Clusters class
        mc = MC_Clusters(thereshold, self)

        # 2.b) append thereshold and cluster to the dictionary
        self.cluster_list[thereshold] = mc

        # 2.c) write results to output
        with h5py.File(self.output_file, 'a') as out_writer:
        
            grp = out_writer.create_group(str(thereshold))
        
            grp.attrs['norm'] = self.norm
            grp.attrs['threshold'] = thereshold
            grp.attrs['n_clusters'] = len(mc.n_points)
        
            dset = grp.create_dataset("n_points", (len(mc.n_points),), dtype='f')
            dset[...] = mc.n_points
            dset = grp.create_dataset("mass", (len(mc.mass),), dtype='f')
            dset[...] = mc.mass
            dset = grp.create_dataset("r_half_max", (len(mc.r_half_max),), dtype='f')
            dset[...] = mc.r_half_max
            dset = grp.create_dataset("r_90pc", (len(mc.r_90pc),), dtype='f')
            dset[...] = mc.r_90pc
            dset = grp.create_dataset("r_mass_weighted", (len(mc.r_mass_weighted),), dtype='f')
            dset[...] = mc.r_mass_weighted
            dset = grp.create_dataset("momentum_of_inertia", (len(mc.momentum_of_inertia),3), dtype='f')
            dset[...] = mc.momentum_of_inertia
            
            out_writer.close()
            print('-> saved results to %s\n' %(self.output_file))

             


