import sys, os
import glob
import re

def collect_sims(folder_in, folder_out):

    # 1. get all potential output folders
    dirlist = next(os.walk(folder_in))[1]

    # 2. initialise final arrays
    sim_name = []
    out_name = []

    # 3. create simulation location and output name
    for dir in dirlist:
        # output name
        on = folder_out + '/' + dir

        #find the final simulation file
        dir = folder_in + '/' + dir + '/m'
        mfile = findsimfile(dir)

        #if there is no correct m-file ignore the folder
        if mfile == '':
            continue
        
        # append to the list of filenames
        sim_name.append(mfile)
        out_name.append(on)

    return sim_name, out_name

def findsimfile(address):
    file = ''
    max = 0
    for filename in glob.iglob(address+'/**axion.m.*'):
        num = int(re.findall(r'\d+', filename)[-1])
        if num > max:
            max = num
            file = filename
    return file ;

