import csv
import h5py

from MC_Clusters import MC_Clusters

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

        # 1.b) initialize variables holding the analysis
        self.cluster_list = dict()

        # 1.c) get information about the simulation
        #      and test if the input file can be opend
        with h5py.File(input_data, 'r') as input:
            self.n = input.attrs[u'Size']
            self.sizeL = input.attrs[u'Physical size']
            self.n3 = self.n*self.n*self.n
            self.zi = input.attrs[u'zInitial']
            self.zf = input.attrs[u'zFinal']
            self.zc = input.attrs[u'z']
            self.llambda = input.attrs[u'Lambda']
            self.nQCD = input.attrs[u'nQcd']
            
            
        # 1.d) create output file & write header
        #      an existing file of the same name will be reased
        self.fieldnames = ['density_th',
                           'n_points',
                           'mass',
                           'r_half_max',
                           'r_90pc',
                           'r_mass_weighted',
                           'momentum_of_inertia']
    
        with open(self.output_file, 'w') as output:
            output.write('# analysis of %s\n' %(self.input_data))
            output.write('# points per grid axis %d\n' %(self.n))
            output.write('# physical grid size %1.1f\n' %(self.sizeL))
            output.write('\n')
            writer = csv.DictWriter(output, fieldnames=self.fieldnames)
            writer.writeheader()

            
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
            writer.writerow({'density_th':thereshold, 'n_points':mc.n_points, 'mass':mc.mass,
                             'r_half_max':mc.r_half_max, 'r_90pc':mc.r_90pc,
                             'r_mass_weighted':mc.r_mass_weighted, 'momentum_of_inertia':mc.momentum_of_inertia})

            print('-> saved results to %s\n' %(self.output_file))
             



