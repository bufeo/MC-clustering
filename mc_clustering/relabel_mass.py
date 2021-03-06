import MC_Simulation
import numpy as np

def getMass(it):
    return it[1]

def relabel_mass(newlabels, den):
    # 1. create a list containing the label and mass(= sum of densities)

    minilabels = np.array(list(set(newlabels)))
    poso = []
    for l in minilabels:
        if l > -1:
            class_member_mask = (newlabels == l)
            poso.append( [l ,np.add.reduce(den[class_member_mask])] )
    
    # 2. sort the lists
    oroM = sorted(poso,key=getMass)

    # 3. create two new arrays for the labels
    numberoflabels = len(oroM)
    masslabels = np.empty_like(newlabels)

    # noise 
    masslabels[:] = newlabels[:]
    
    counter = 0 

    # 4. assign labels ordered by mass
    for i in range(0,numberoflabels):
        para = (newlabels == oroM[i][0])
        masslabels[para] = numberoflabels-i-1
    
    return masslabels
    
