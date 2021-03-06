import numpy as np
import sys
from numpy import linalg as LA

def reshift_to_1(label, masslabels, pos, n):
    # this function is to be called from sosa
    
    # 1. extract positions of the affected cluster
    cordi = pos[masslabels == label]
    
    # 2. iterate over directions
    shift_vector = [0,0,0]
    for axis in range(0,3):
        
        # 2.a) get the set of coordinates in one direction
        coordinates_1d = sorted(set(cordi[:,axis]))
                
        # 2.b) check if the direction needs a shift
        if coordinates_1d[0] == 0 and coordinates_1d[-1] == n-1:
            
            #2.c) find the right magnitude for the shift
            # all coordinates which are not in the list
            free_points = [x for x in xrange(0,n) if x not in coordinates_1d]
            
            found_free_plane = False
            counter = len(free_points)-1
            while not found_free_plane:
                shift = free_points[counter]
                
                # we require that the shifted grid has no cluster on any boundaries!
                if (shift-1) == free_points[counter-1]:
                    shift_vector[axis] = n-shift
                    found_free_plane = True
                else:
                    counter = counter-1
                if counter==0:
                    print('Trying to shift the cluster with masslabel %d:' %(label))
                    print('FAILED: could not find a free plane in direction %d.' %(axis))
                    print('excluding the cluster from the analysis')
                    return []
                
    # 3. apply all three shifts to the cluster
    cordi = np.add(cordi, shift_vector)%n
    
    return cordi, shift_vector

def cluster_com(label, masslabels, pos, den, n):
    
    cordi, shift_vec = reshift_to_1(label, masslabels, pos, n)
    lden  = den[masslabels == label]
    
    # compute the COM (in reshifted coordinates)
    masa  = np.add.reduce(lden)
    momi = np.empty_like(cordi)
    momi[:,0] = lden*cordi[:,0]
    momi[:,1] = lden*cordi[:,1]
    momi[:,2] = lden*cordi[:,2]
    com1 = np.add.reduce(momi)/(masa)
    
    return com1, shift_vec    

def analyse_mcs(masslabels, den, labels, labels2, pos, Sim):

    print '-> analyzing clusters...',
    sys.stdout.flush()
    
    dapa =[]
    pain =[]
    mcl_it = set(masslabels)
    mcl_it.discard(-1)
    
    for mcl in mcl_it:
        
        cordi, vec = reshift_to_1(mcl, masslabels, pos, Sim.n)

        # 2.c) check if the cluster contains more than one point
        # this is not the case when reshift_to_1 fails to find an appropriate plane
        if len(cordi) > 1: 
            
            # 2.d) get mass and number of points
            lden  = den[masslabels == mcl]
            masa  = np.add.reduce(lden)
            numb  = np.add.reduce(masslabels == mcl)

            # 2.e) compute the center of motion & place it in the origin
            com1, vec = cluster_com(mcl, masslabels,pos, den, Sim.n)
            #momi = np.empty_like(cordi)
            relcor = np.empty_like(cordi)
            #momi[:,0] = lden*cordi[:,0]
            #momi[:,1] = lden*cordi[:,1]
            #momi[:,2] = lden*cordi[:,2]
            #com1 = np.add.reduce(momi)/(masa)
            relcor = cordi - com1 
            
            # 2.f) compute radius (3 different definitions)
            radii = LA.norm(relcor,axis=1)
            top = int(max(radii) ) + 1 
            r1 = max(radii)/2
            r2 = (np.add.reduce(radii*radii*lden)/masa)**0.5
            # r3 = np.add.reduce(radii*lden)/masa

            # 2.g) the density profile
            bins=range(0,top)
            bin_d = (np.histogram(radii, bins, weights=lden)[0])
            ms = np.cumsum(bin_d/masa)
            ms = np.append(ms,1.)

            # 2.h) radius which includes 90% of the density
            per1 = 0.9
            rad = np.arange(0,len(ms))
            low = ms[ms<per1][-1]
            rr1 = rad[ms<per1][-1]
            hig = ms[ms>per1][0]
            rr2 = rad[ms>per1][0]
            r4 = rr1 + (per1-low)*(rr2-rr1)/(hig-low)

            # 2.i) a meassure for sphericity
            misa = np.identity(3)*0
            for i in range(0,len(relcor)):
                fus = relcor[i]
                misa = misa + lden[i]*(np.dot(fus,fus)*np.identity(3) - np.outer(fus,fus))
            maino = np.sqrt(LA.eigvalsh(misa)/masa)

            dapa.append([numb,masa,r1,r2,r4])
            pain.append(maino)
                
        else:
            print('WARNING: the cluster with label %d contains 0 or 1 points' %(mcl))
            print('either the function reshift_to_1 failed or your clustering is erronous!')
            
    dapa = np.array(list(dapa))
    pain = np.array(list(pain))

    print('done')
    
    return dapa, pain
