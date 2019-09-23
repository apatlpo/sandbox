
    #!/usr/bin/python
# -*- coding:Utf-8 -*-

import sys
import glob
import os
import numpy as np
#import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
#import matplotlib.collections as col
import numpy.ma as ma




def plot_colorline(x,y,c):
    c = cm.jet((c-np.min(c))/(np.max(c)-np.min(c)))
    ax = plt.gca()
    for i in np.arange(len(x)-1):
        ax.plot([x[i],x[i+1]], [y[i],y[i+1]], c=c[i])
    #plt.colorbar(line,ax=ax)
    return


def plot_colorline(x,y,c):
    """
    Plots XY Plot of given trajectory, with color as a function of c
    """

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(c.min(), c.max())
    lc = LineCollection(segments, cmap='RdYlBu', norm=norm)
    # Set the values used for colormapping
    lc.set_array(c)
    lc.set_linewidth(2)

    ax = plt.gca()
    line = ax.add_collection(lc)
    fig.colorbar(line, ax=ax)
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    # ax.set_xlim(1, 256)
    # ax.set_ylim(1, 720)

    return

def get_floats(dpath):
#
# load float data, written by wrt_floats_mpi.F
#
    # float directory in directory dpath
    files = glob.glob(dpath+'/float.????')
    # Files in subdirectories t1,t2,...
    if len(files) == 0:
        files=[]
        # tpath = glob.glob(dpath+'/t[1-9]*/')
        tpath = glob.glob(dpath+'/t[1-3]*/')
        for idir in range(len(tpath)):
            dirfiles = glob.glob(tpath[idir]+'/float.????')
            files.append(dirfiles)
        # flatten list
        files = [item for sublist in files for item in sublist]

    if len(files)>0: 
        flagflt=0
        for file in files:
            if os.path.getsize(file) > 0:
                try:
                    M = np.concatenate((M, np.asarray(np.loadtxt(file))), axis=0)
                except:
                    M = np.asarray(np.loadtxt(file))
    
    # number of different values in first collumn which is number of floats
        nfloats=len(np.unique(M[:,0]))
        numfloat = np.unique(M[:,0])
        print('nfloats=',nfloats)
        # print('numfloat=',numfloat)

        Df = []
        # For each float
        for iflt in range(nfloats):
            # extract flotteur iflt
            Miflt = np.squeeze(M[np.where(M[:,0] == numfloat[iflt])])
            # Sort by time
            Miflt = np.squeeze(np.asarray(sorted(Miflt, key=lambda x : x[1])))
            # Store in dictionnary
            Diflt = {}
            Diflt['float'] = Miflt[:,0]
            Diflt['time'] = Miflt[:,1]
            Diflt['xgrid'] = Miflt[:,2]
            Diflt['ygrid'] = Miflt[:,3]
            Diflt['zgrid'] = Miflt[:,4]
            Diflt['depth'] = Miflt[:,5]
            Diflt['temp'] = Miflt[:,6]
            # Append dictonnary to array of floats
            Df.append(Diflt)
            

    return nfloats,Df


# dpath = "/home1/dunree/slgentil/models/croco/croco/CONFIGS/Run_JETN/"
# dpath = "/home/datawork-lops-osi/slgentil/croco/jetn/jet_cfg1_wp75_4km_1500a2500j_float/t1"
dpath = "/home1/scratch/slgentil/jet_cfg1_wp75_4km_1500a2500j_float/t1"
nfloats,Df = get_floats(dpath)

# for iflt in range(nfloats):
# for iflt in range(10,900,100):
for iflt in range(210,211):

    # insert None point if float jump from East/West
    for index in range(Df[iflt]['xgrid'].size-1):
        if abs(Df[iflt]['xgrid'][index+1] - Df[iflt]['xgrid'][index]) > 250 :
            Df[iflt]['xgrid'] = ma.masked_invalid(np.insert(Df[iflt]['xgrid'],index+1,np.NaN))
            Df[iflt]['ygrid'] = ma.masked_invalid(np.insert(Df[iflt]['ygrid'],index+1,np.NaN))
            Df[iflt]['temp'] = ma.masked_invalid(np.insert(Df[iflt]['temp'],index+1,np.NaN))

    fig=plt.figure()

    # plot 2D line(x,y)
    # plt.plot(Df[iflt]['xgrid'][::24],Df[iflt]['ygrid'][::24])
    # plt.axis([1, 128, 1, 360]) 


    # plot 2D line (x,y) colored with temp
    inc=24
    plot_colorline(Df[iflt]['xgrid'][::inc],Df[iflt]['ygrid'][::inc],Df[iflt]['temp'][::inc])
    # plot_colorline(Df[iflt]['xgrid'],Df[iflt]['ygrid'],Df[iflt]['temp'])

    # plot 3D line (x,y,z)
    # ax = fig.gca(projection='3d')
    # ax.plot(Df[iflt]['xgrid'],Df[iflt]['ygrid'],Df[iflt]['depth'])

    title = 'float {:4d}, initial position ({:6.1f},{:6.1f}),time {:6.1f} to {:6.1f} days'.format(int(Df[iflt]['float'][0]),\
            Df[iflt]['xgrid'][0],Df[iflt]['ygrid'][0],Df[iflt]['time'][0],Df[iflt]['time'][-1])
    plt.title(title)

plt.show()
