from extract_above_th import extract_above_th
from analyse_mcs import cluster_com

import numpy as np
from numpy import linalg as LA


def density_profile(mcs, lmc):

    # compute the COM & possible coordinate shift
    com1, shift_vec = cluster_com(lmc, mcs.masslabels, mcs.pos, mcs.den, mcs.n)
    
    # define the maximum radius
    radius= mcs.r_90pc[lmc]
    rmax = 1.5*radius

    #obtain the full grid
    # does this work??
    pos_A, den_A, _, _, = extract_above_th(0, mcs)

    # shift the full grid so the COM is in the middle (at [n/2 n/2 n/2])
    tmp_vec = np.ones(3)*float(mcs.n//2)
    shift_vec = shift_vec + tmp_vec - com1
    pos_A = np.add(pos_A, shift_vec)%mcs.n

    # only keep a square around the com
    # this only serves for data reduction
    tmp_vec_min = np.ones(3)*(mcs.n//2 - rmax)
    tmp_vec_max = np.ones(3)*(mcs.n//2 + rmax)
    
    # if the cluster is too big take the whole grid
    if any(tmp_vec_min < 0) or any(tmp_vec_max > (mcs.n-1)):
        tmp_vec_min[:] = 0
        tmp_vec_max[:] = mcs.n-1
    
    map_square = np.all(np.greater(pos_A,tmp_vec_min),axis=1)*(np.all(np.less(pos_A,tmp_vec_max),axis=1))
    pos_A = pos_A[map_square]
    den_A = den_A[map_square]

    # compute distance to the COM
    tmp_vec = np.ones(3)*float(mcs.n//2)
    radii = LA.norm(pos_A-tmp_vec,axis=1)

    # compute average density within each radius bin
    nbin = 10
    density_profile = np.zeros(nbin)
    radii_profile = np.zeros(nbin)
    sum_points = 0
    sum_den = 0
    
    for rbin in range (0,nbin):
        b_min = (rbin)/float(nbin)*rmax
        b_max = (rbin+1)/float(nbin)*rmax
        
        # for small mcs the innermost radius is too small!
        map_bin = (radii>b_min)*(radii<b_max)
        if np.add.reduce(map_bin) > 0:
            sum_points += np.add.reduce(map_bin)
            sum_den += np.add.reduce(den_A[map_bin])
                
            density_profile[rbin] = sum_den/sum_points
            radii_profile[rbin] = b_max/radius
        
    return density_profile, radii_profile

    
    ##################################################
    
    
    
        
    
