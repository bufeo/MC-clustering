import sys

import MC_Simulation
from extract_above_th import extract_above_th
from find_clusters import find_clusters
from join_boundaries import join_boundaries
from relabel_mass import relabel_mass
from analyse_mcs import analyse_mcs
from analyse_mcs import cluster_com
from analyse_mcs import reshift_to_1
from density_profile import density_profile

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_pdf

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec
import matplotlib.lines as mlines
from matplotlib.legend_handler import HandlerLine2D

class MC_Clusters:
    """Clustering of a simulation for one thereshold"""

    ##############################
    # 1. Constructor
    ##############################
    def __init__(self, dens_th, Sim):

        self.info = {}

        # 1.a) extract all points above thereshold
        print 'extracting points above threshold...',
        sys.stdout.flush()
        
        self.pos, self.den, self.info['number of points'], self.info['fraction of mass'] = extract_above_th(dens_th, Sim)
        print('done')
    
        # 1.b) cluster original and shifted set
        labels, labels2 = find_clusters(self.pos, Sim)
        self.info['nMCs first iteration'] = str(len(set(labels))-1)
        self.info['nMCs second iteration'] = str(len(set(labels2))-1)

        # 1.c) join periodic boundaries
        newlabels = join_boundaries(labels, labels2)
        
        # 1.d) find labels ordered by mass
        self.masslabels = relabel_mass(newlabels, self.den)

        # 1.e) analyse the miniclusters:
        #      mass
        #      number of points
        #      radius
        #      momentum of inertia
        mnr, moi = analyse_mcs(self.masslabels, self.den, labels, labels2, self.pos, Sim)

        # 1.f) save all information to the class
        self.n = Sim.n
        self.n3 = (self.n)**3
        self.sizeL = Sim.sizeL
        self.density_th = dens_th
        self.input_data = Sim.input_data
        self.output_data = Sim.output_file
        self.plot_file = Sim.output_prefix + '_th-' +  str(self.density_th) + '_plots.pdf'
        self.n_points = mnr[:,0]
        self.mass = mnr[:,1]
        self.r_half_max = mnr[:,2]
        self.r_mass_weighted = mnr[:,3]
        self.r_90pc = mnr[:,4]
        self.momentum_of_inertia = moi


    ##############################
    # 2. Plotting for individual analysis
    #    mass vs radius
    ##############################

    def plot_mass_vs_radius(self,r_type):
        delta = self.sizeL/self.n
        unitmass = (delta)**3

        if r_type == 1:
            radius = self.r_half_max
            r_string = 'Half maximum radius [$r/H_1 R_1$]'
        elif r_type == 2:
            radius = self.r_mass_weighted
            r_string = 'Mass weighted radius [$r/H_1R_1$]'
        elif r_type == 3:
            radius = self.r_90pc
            r_string = 'Radius containing 90% of the total mass [$r/H_1R_1$]'
        else:
            print('choice of radius type not valid')
            return 0
            
        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt.yscale('log')
        plt.xscale('log')
        plt.ylabel(r_string)
        plt.xlabel('Mass [$M_1$]')
        ax.set_xlim(.5*unitmass*min(self.mass),2*unitmass*max(self.mass))
        ax.set_ylim(.5*delta*min(radius),2*delta*max(radius))
        
        plt.scatter(unitmass*self.mass,delta*radius, c='green', lw=0,rasterized=True)

        # a line for orientation
        mid = len(radius)//2
        r_mid = delta*radius[mid]
        m_mid = unitmass*self.mass[mid]
        x = delta*np.linspace(min(radius),max(radius),10)
        plt.plot( m_mid*(x/r_mid)**3, x, c='blue', alpha=0.2,rasterized=True)
                
        return fig

    ##############################
    # 3. Plotting for individual analysis
    #    excentricity histogramm
    ##############################
    def plot_excentricity_histogram(self):
        fig = plt.figure()
        
        ecc = []
        for i in range(0,len(self.momentum_of_inertia)):
            mix = min(self.momentum_of_inertia[i])
            man = max(self.momentum_of_inertia[i])
            ecc.append((man-mix)/(man+mix))
            
        weights = np.ones_like(ecc)/float(len(ecc))    
        plt.xlabel('eccentricity $(I_3-I_1)/(I_3+I_1)$')    
        plt.hist(ecc,bins=np.linspace(0,1,20), lw=0, weights=weights)
        return fig
    
    ##############################
    # 4. plot mass histogram
    ##############################
    def plot_mass_histogram(self):

        fig = plt.figure()
        delta = self.sizeL/self.n
        unitmass = delta**3
        weights = np.ones_like(self.mass)/float(len(self.mass))
        plt.xscale('log')
        plt.xlabel('mass [$M_1$]')
        plt.hist(unitmass*self.mass,bins=np.logspace(-5,1,20), lw=0,weights=weights)

        return fig    
    

    ##############################
    # 5. Summarize plotting to pdf
    ##############################

    def plot_all(self):

        with matplotlib.backends.backend_pdf.PdfPages(self.plot_file) as pdf:

            print 'plotting file %s for threshold %1.1f' %(self.input_data, self.density_th)
            print 'descrition text...',
            sys.stdout.flush()
            # write some information about the analysis
            fig = plt.figure()
            ax = fig.add_subplot(111)
            fig.subplots_adjust(top=0.85)
            ax.axis('off')

            description =  'data file: ' + self.input_data + '\n'
            description += 'results saved to: ' + self.output_data + '\n'
            description += 'points per axis: ' + str(self.n) + '\n'
            description += 'physical grid size: ' + str(self.sizeL) + '\n\n'

            description += 'For density threshold ' + str(self.density_th) + ':\n'
            description += '* found %d points' %(self.info['number of points']) + '\n'
            description += '* containing %2.2f%% of the total mass' %(self.info['fraction of mass']) + '\n\n'

            description += 'clustering the data gave:\n'
            description += '# of clusters found in 1st iteration: ' + self.info['nMCs first iteration'] + '\n'
            description += '# of clusters found in 2nd iteration: ' + self.info['nMCs second iteration'] + '\n'
            description += '# of clusters found after accounting for periodic boundaries: ' + str(len(self.mass)) + '\n'
            
            ax.text(0.01, 1.0, description,
                    verticalalignment='top', horizontalalignment='left',
                    transform=ax.transAxes,
                    fontsize=12)

            pdf.savefig( fig )
            plt.close(fig)
            print 'done'

            
            # mass vs. radius plot
            print 'mass vs. radius...',
            sys.stdout.flush()
            
            for i in range(1,4):
                fig = self.plot_mass_vs_radius(i)
                pdf.savefig( fig )
                plt.close(fig)
            print 'done'

            # eccentricity histogramm
            print 'eccentricity histogramm...',
            fig = self.plot_excentricity_histogram()
            pdf.savefig( fig )
            plt.close(fig)
            print 'done'

            # mass histogram
            print 'mass histogramm...',
            sys.stdout.flush()
            
            fig = self.plot_mass_histogram()
            pdf.savefig( fig )
            plt.close(fig)
            print 'done'

            # the 5 heaviest clusters
            print 'the 5 heaviest clusters...',
            sys.stdout.flush()
            
            for i in range(0,5):
                fig = self.plot_individual_cluster(i)
                pdf.savefig( fig )
                plt.close(fig)
            print 'done'

            #density profile
            print 'density profile...',
            sys.stdout.flush()
            
            fig=self.plot_density_profiles()
            pdf.savefig(fig)
            plt.close(fig)
            print 'done'

            print '-> saved plots to %s\n' %(self.plot_file)

    ##############################
    # 6. plot spatial distributio of a cluster
    ##############################
    def plot_individual_cluster(self,label):
    
        # com and radii
        com,v = cluster_com(label, self.masslabels, self.pos, self.den, self.n)
        r_1 = self.r_half_max[label]
        r_2 = self.r_mass_weighted[label]
        r_3 = self.r_90pc[label]
    
        # plotting environment
        gs = gridspec.GridSpec(3, 2, width_ratios=[3, 1])
        fig = plt.figure(figsize=(10,8))
        
        # 3D plot
        ax1 = fig.add_subplot(gs[0:2,0],projection='3d')
        xyz, v = reshift_to_1(label,self.masslabels,self.pos,self.n)
        ax1.set_xlim3d(min(xyz[:,0]), max(xyz[:,0]))
        ax1.set_ylim3d(min(xyz[:,1]), max(xyz[:,1]))
        ax1.set_zlim3d(min(xyz[:,2]), max(xyz[:,2]))
        ax1.scatter3D(xyz[:,0], xyz[:,1], xyz[:,2],lw=0,c='blue',depthshade='True',alpha=.1,rasterized=True)
        ax1.scatter(com[0],com[1],com[2],c='red',lw=0,rasterized=True)


        # projection 1
        circle1 = plt.Circle((com[0],com[1]), r_1, color='black',fill=False,lw=.2 )
        circle2 = plt.Circle((com[0],com[1]), r_2, color='black',fill=False,lw=1,linestyle='--')
        circle3 = plt.Circle((com[0],com[1]), r_3, color='black',fill=False,lw=1,linestyle=':')

        ax2 = fig.add_subplot(gs[0,1])
        ax2.scatter(xyz[:,0], xyz[:,1],lw=0,c='blue',alpha=.3,rasterized=True)
        ax2.scatter(com[0],com[1],c='red',lw=0,rasterized=True)
        ax2.set_xticklabels([])
        ax2.set_yticklabels([])
        ax2.set_xlim([com[0]-2*r_1, com[0]+2*r_1])
        ax2.set_ylim([com[1]-2*r_1, com[1]+2*r_1])
        ax2.set_aspect('equal')
        ax2.add_artist(circle1)
        ax2.add_artist(circle2)
        ax2.add_artist(circle3)

        # projection 2
        circle1 = plt.Circle((com[0],com[2]), r_1, color='black',fill=False,lw=.2)
        circle2 = plt.Circle((com[0],com[2]), r_2, color='black',fill=False,lw=1,linestyle='--')
        circle3 = plt.Circle((com[0],com[2]), r_3, color='black',fill=False,lw=1,linestyle=':')

        ax3 = fig.add_subplot(gs[1,1])
        ax3.scatter(xyz[:,0], xyz[:,2],lw=0,c='blue',alpha=.1,rasterized=True)
        ax3.scatter(com[0],com[2],c='red',lw=0,rasterized=True)
        ax3.set_xticklabels([])
        ax3.set_yticklabels([])
        ax3.set_xlim([com[0]-2*r_1, com[0]+2*r_1])
        ax3.set_ylim([com[2]-2*r_1, com[2]+2*r_1])
        ax3.set_aspect('equal')
        ax3.add_artist(circle1)
        ax3.add_artist(circle2)
        ax3.add_artist(circle3)

        # projection 3
        circle1 = plt.Circle((com[1],com[2]), r_1, color='black',fill=False,lw=.2)
        circle2 = plt.Circle((com[1],com[2]), r_2, color='black',fill=False,lw=1,linestyle='--')
        circle3 = plt.Circle((com[1],com[2]), r_3, color='black',fill=False,lw=1,linestyle=':')

        ax4 = fig.add_subplot(gs[2,1])
        ax4.scatter(xyz[:,1], xyz[:,2],lw=0,c='blue',alpha=.1,rasterized=True)
        ax4.scatter(com[1],com[2],c='red',lw=0,rasterized=True)
        ax4.set_xticklabels([])
        ax4.set_yticklabels([])
        ax4.set_xlim([com[1]-2*r_1, com[1]+2*r_1])
        ax4.set_ylim([com[2]-2*r_1, com[2]+2*r_1])
        ax4.set_aspect('equal')
        ax4.add_artist(circle1)
        ax4.add_artist(circle2)
        ax4.add_artist(circle3)
    
        # description
        ax5 = fig.add_subplot(gs[2,0])
        ax5.axis('off')
    
        # radii
        label_r_1 = 'half maximum radius = %1.2f $\\times H_1 R_1$' %(self.sizeL/self.n*r_1)
        line_r_1  = mlines.Line2D([], [], color='black', lw=.2, label=label_r_1)
        label_r_2 = 'mass weighted radius = %1.2f $\\times H_1 R_1$' %(self.sizeL/self.n*r_2)
        line_r_2  = mlines.Line2D([], [], color='black', lw=1,linestyle='--', label=label_r_2)
        label_r_3 = 'radius enclosing 90%% of cluster mass  = %1.2f $\\times H_1 R_1$' %(self.sizeL/self.n*r_3)
        line_r_3  = mlines.Line2D([], [], color='black', lw=1,linestyle=':', label=label_r_3)
    
        # COM
        label_com = 'center of mass'
        line_com = mlines.Line2D([], [], c='red',lw=0, marker='o', label=label_com)
    
        legend = plt.legend(handles=[line_r_1,line_r_2, line_r_3, line_com],
                            handler_map = {line_com: HandlerLine2D(numpoints=1)},
                            frameon=False)
        legend._legend_box.align = "left"
    
        # title
        if label==0:
            titlestring = 'Heaviest '
        elif label==1:
            titlestring = '2nd heaviest '
        elif label==2:
            titlestring = '3rd heaviest '
        else:
            titlestring ='%d th heaviest ' %(label+1)

        titlestring += 'cluster found for a thereshold of ' + str(self.density_th) +  '.\n'
        titlestring += 'Cluster mass: %1.2f $\\times M_1$, number of points: %d .' %((self.sizeL/self.n)**3*self.mass[label],
                                                                                         self.n_points[label])
    
        legend.set_title(titlestring,prop = {'size':'large'})
        gs.update(wspace=.1, hspace=.1)
        return fig

    ##############################
    # 8. plot density profiles
    ##############################
    def plot_density_profiles(self):

        profiles = []
        bins = []

        for i in range(0,5):
            p, b = density_profile(self, i)
            profiles.append(p)
            bins.append(b)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt.xlabel('radius [$r/r_{90pc}$]')
        plt.ylabel('$\delta_{av}(r)$')

        plt.plot(bins[0], profiles[0], marker='o', label='Heaviest MC')
        plt.plot(bins[1], profiles[1], marker='o', label='2nd heaviest MC')
        plt.plot(bins[2], profiles[2], marker='o', label='3rd heaviest MC')
        plt.plot(bins[3], profiles[3], marker='o', label='4th heaviest MC')
        plt.plot(bins[4], profiles[4], marker='o', label='5th heaviest MC')

        legend = plt.legend(bbox_to_anchor=(1.1, 1),numpoints=1)

        return fig
