import h5py
import MC_Simulation
import numpy as np

def extract_above_th(dens_th, Sim):

    n = Sim.n
    n3 = Sim.n3
    
    # extract data from file
    with h5py.File(Sim.input_data, 'r') as input:
        data = input['energy/density'].value.reshape(n3)

    # mask all points below the density thereshold
    mask = ( data > dens_th)

    # auxiliary position array
    bas = np.zeros((n,n,n),dtype=float)
    linap = np.arange(0,n,dtype=float).reshape((n,1,1))
    x_pos = bas + linap
    y_pos = bas + linap.reshape((1,n,1))
    z_pos = bas + linap.reshape((1,1,n))
    del bas, linap
    x_pos = np.reshape(x_pos,(n3,))
    y_pos = np.reshape(y_pos,(n3,))
    z_pos = np.reshape(z_pos,(n3,))

    # create an empty array to hold the positions
    npo = len(x_pos[mask])
    pos = np.empty((npo,3))
    
    # apply mask to only get the positions above thereshold
    # write to position array
    pos[:,0] = x_pos[mask]
    pos[:,1] = y_pos[mask]
    pos[:,2] = z_pos[mask]
    
    #apply mask to get the density array
    den = data[mask]
    
    fractionofmass = np.add.reduce(den)/n3
    
    return pos, den, npo, fractionofmass
