import numpy as np
import h5py

########## Find normalization factor ##########
# if an normalisation factor is provided in the Sim-constructor use it
# for using pre-normalized data give norm=1
# default: norm = average density over simulation box
def find_norm(Sim):

    # apply the normalization:
    # if external normalisation is provided use it
    if Sim.norm > 0:
        norm = Sim.norm

    # if no external normalization is provided use
    # the average of the simulation box
    else:
        with h5py.File(Sim.input_data, 'r') as input:
            try:
                data = input['energy/redensity'].value.reshape(Sim.n3)
            except KeyError:
                data = input['energy/density'].value.reshape(Sim.n3)
        norm = np.average(data)

    return norm

########## Find # of points per grid axis ##########
def find_n(Sim):
    with h5py.File(Sim.input_data, 'r') as input:
        try:
            nn = int(np.cbrt(len(input['energy/redensity'])))
        except KeyError:
            nn = int(np.cbrt(len(input['energy/density'])))

    return nn
