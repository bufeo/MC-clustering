import numpy as np

def join_boundaries(labels, labels2):

    print '-> accounting for periodic boundaries...',
    npo = len(labels)
        
    # 1. create auxilliary label arrays
    # conventions: points already visited are -2 in labels11, labels22
    #              points not visited yet are -2 in newlabels
    newlabels = np.zeros(npo,dtype=int) -2
    labels11 = np.zeros(npo,dtype=int)
    labels22 = np.zeros(npo,dtype=int)
    
    labels11[:] = labels
    labels22[:] = labels2
    
    # account for all points which are marked as noise in both datasets
    parla1 = (labels  == -1)
    parla2 = (labels2 == -1)

    newlabels[parla1*parla2]   = -1
    labels11[parla1*parla2] = -2
    labels22[parla1*parla2] = -2
  
    # 2. create a list with the first index at which a label appears
    m1 = max(labels)
    jta = np.arange(0,npo,dtype=int)

    po1 = []
    for j in set(labels):
        if j > -1:
            parla1 = (labels  == j)
            po1.append(jta[parla1][0])
    po1 = np.array(po1)
       
    # 3. loop over all clusters found in set1    
    for i in set(labels): 
        if i > -1:
            # reference point
            posi = po1[i]
            ll = labels[posi]
            
            # get the cluster of this point in both labeling systems
            parla1 = (labels  == ll)
            parla2 = (labels2 == labels2[posi])
               
            # if the point labels two clusters, group them
            if labels2[posi] > -1 :
                mask = np.logical_or(parla1,parla2)
                seta = np.array(list(set(newlabels[mask])))
                seta = seta[seta > -1]
                               
                # actually some of the points found may already be part of a cluster
                # account for all points in that cluster
                # changed from Javiers original code
                # if len(seta) > 1:
                if len(seta) > 0:
                    for lset in seta:
                        minimask = (newlabels == lset)
                        mask = np.logical_or(mask,minimask)
                    ll = min(seta)
                    
                newlabels[mask] = ll
                labels11[mask] = -2
                labels22[mask] = -2
                                
            # if the point belongs to a mc in case 1 but not in case 2:
            # only take the points from case 1 & edit in newlabels
            # the opposite case is accounted for below
            elif labels2[posi] == -1 :
                mask = parla1 
                newlabels[mask] = ll
                labels11[mask] = -2
            
    maxrelab = max(newlabels)

    # 4. account for points which are noise in set1 but belong to a cluster in set2
    rela2 = np.array(list(set(labels22)))

    counter = 0
    
    for j in rela2:
        if j > -1 :
            # must anypoint of this MC need be asssotiated with a mc already present in newlabels?
            # changed from Javiers initial code
            # asolabel = np.array(list(set(labels2[parla22])))
            # parla22 = (labels22  == j)
            parla22 = (labels2 == j)
            asolabel = np.array(list(set(newlabels[parla22])))
            asolabel = asolabel[asolabel > -1]
            
            ll2 = j
            
            # changed from Javiers original code:
            #if asolabel == []
            #if not asolabel.any():
            if len(asolabel)==0:
                # changed from Javiers initial code
                # first increase the counter THEN assign the label
                counter +=1 
                newlabels[parla22] = maxrelab + counter
                
            elif len(asolabel) > 0:
                lala = min(asolabel)

                for l in asolabel:
                    para = (newlabels == l)
                    newlabels[para] = lala
                
                newlabels[parla22] = lala
                
            labels11[parla22] = -2
            labels22[parla22] = -2    

    if (sum(newlabels==-2)) > 0:
        print('\nWARNING: join_boundaries did not visit %d points!'%(sum(newlabels==-2)))
        print('This might be a possible bug!\n')

    print('done')

    return newlabels

