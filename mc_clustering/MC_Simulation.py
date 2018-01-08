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
        self.output_file = output_prefix + '.csv'
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
        #      create output file & write header
        #      an existing file of the same name will be erased
        if self.preexists == False:
            self.fieldnames = ['density_th',
                               'norm',
                               'n_points',
                               'mass',
                               'r_half_max',
                               'r_90pc',
                               'r_mass_weighted',
                               'momentum_of_inertia']
    
            with open(self.output_file, 'w') as output:
                output.write('# %s\n' %(self.input_data))
                writer = csv.DictWriter(output, fieldnames=self.fieldnames)
                writer.writeheader()

        # 1.c) if there is a pre-existing output file:
        #      check it refers to the correct data file
        #      and read in all analysis from it
        else:
            with open(self.output_file, 'r') as output:
                ifile = output.readline()
                ifile = ifile[2:].strip()

                # check the input file is correct
                if ifile != self.input_data:
                    print('\nERROR in reading data from a previous analysis:')
                    print('File names given as argument and read from data not matching!')
                    print('Aborting computation.\n')
                    exit()

                #read in data for the individual clusters
                reader = csv.DictReader(output)
                for row in reader:
                    
                    # call the constructor to get all basic information
                    thereshold = float(row['density_th'])
                    mc = MC_Clusters(thereshold, self, preexists=True)

                    # assign data read from file
                    mc.norm = float(row['norm'])
                    mc.n_points            = string_to_array(row['n_points'],            1)
                    mc.mass                = string_to_array(row['mass'],                1)
                    mc.r_half_max          = string_to_array(row['r_half_max'],          1)
                    mc.r_mass_weighted     = string_to_array(row['r_mass_weighted'],     1)
                    mc.r_90pc              = string_to_array(row['r_90pc'],              1)
                    mc.momentum_of_inertia = string_to_array(row['momentum_of_inertia'], 3)
                  
                    # append to the cluster list
                    self.cluster_list[thereshold] = mc
                    print('-> data file: %s, simulation file: %s, threshold %1.2f' %(ifile ,self.output_file, float(thereshold)))

                    
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
        with open(self.output_file, 'a') as output:
            writer = csv.DictWriter(output, fieldnames=self.fieldnames)
            mom = ''.join(str(e) for e in mc.momentum_of_inertia)
            writer.writerow({'density_th':thereshold, 'norm':self.norm, 'n_points':mc.n_points, 'mass':mc.mass,
                             'r_half_max':mc.r_half_max, 'r_90pc':mc.r_90pc,
                             'r_mass_weighted':mc.r_mass_weighted, 'momentum_of_inertia':mom})
            
            print('-> saved results to %s\n' %(self.output_file))
             


##############################
# some functionality to read miniclusters from file
# only used if preexists == True
##############################
def string_to_array(string, ndim):

    if ndim == 1:
        array = string.split()
        array[-1] = array[-1].replace(']','')
        array = [float(s) for s in array[1:]]
        array = np.array(array)

    elif ndim == 3:
        print(string)
        string = string.replace(']','')
        string = string.replace('[','')
        string = string.replace('\n','')
        print(string.split())        
        string = [float(s) for s in string.split()]
        
        array = []       
        for i in range(0, len(string)/3):
            ar0 = string[3*i]
            ar1 = string[3*i + 1]
            ar2 = string[3*i + 2]
            array.append([ar0, ar1, ar2])
            
    return array
