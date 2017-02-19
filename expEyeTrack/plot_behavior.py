# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:17:50 2017

@author: root
"""

import csv
import numpy as np
#import matplotlib.pyplot as plt
#import plotly.plotly as py
from matplotlib import pyplot

header_dir = "/home/adam/Desktop/py_stimuli/expEyeTrack/headers/"
header_nm = ["hdr02162017_1833","hdr02162017_1825","hdr02162017_1821",
"hdr02162017_1818","hdr02162017_1815","hdr02162017_1811"][::-1]
fig_dir = "/home/adam/Desktop/py_stimuli/expEyeTrack/beh_figs/"

pyplot.figure()     
for H_i, H_nm in enumerate(header_nm):
    
    f_names = []
    correct = []
    f = open(header_dir + H_nm + ".csv", 'rb')
    try:
        reader = csv.reader(f)
        for row in reader:
            f_names.append(row[2])
            correct.append(row[9])
    finally:
        f.close()   
    
    # Extract identity numbers from video list
    ident_ind = f_names[0].find("identity")+len("identity")
    #IDENT_LIST = np.unique([x[ident_ind] for x in f_names],return_inverse = True)[1]
    
    # Correct identity # for faces more than 50% along tang. trajectory
    TRAJ_LIST = np.unique([x[ident_ind+1:ident_ind+4] for x in f_names],return_inverse = True)[1]
    STEP_LIST = np.unique([x[ident_ind+5:ident_ind+8] for x in f_names],return_inverse = True)[1]
    # ['025', '050', '075', '100', 'd.a', 'ly.']
    
#    np.asarray(f_names)[np.where(STEP_LIST>3)]
#    np.asarray(correct)[np.where(STEP_LIST>3)]
    
    foo = np.asarray(correct)[np.where(STEP_LIST>3)]
    rad_results = [np.mean(map(int, foo[foo!='']))]
    for i in range(4):
        foo = np.asarray(correct)[np.where((TRAJ_LIST==1)&(STEP_LIST==i))]
        rad_results.append(np.mean(map(int, foo[foo!=''])))
       
#    np.asarray(f_names)[np.where((TRAJ_LIST==2)&(STEP_LIST==i))]
    tan_results = []
    for i in range(3):
        foo = np.asarray(correct)[np.where((TRAJ_LIST==2)&(STEP_LIST==i))]
        tan_results.append(np.mean(map(int, foo[foo!=''])))
    
    foo = np.asarray(correct)[np.where((TRAJ_LIST==1)&(STEP_LIST==3))]
    tan_results.append(np.mean(map(int, foo[foo!=''])))
    
    x1 = np.asarray(rad_results)
    x2 = np.asarray(tan_results)
    
#    pyplot.clf()
    ax1 = pyplot.subplot(1,2,1)
    x = np.asarray(range(len(x1)))/(len(x1)-1.0)
    pyplot.plot(x,x1,color=pyplot.cm.hot(H_i*30),lw=2)
    pyplot.ylim([0,1])
    pyplot.xticks(x)
    pyplot.title('Radial traj.')
    
    pyplot.subplot(1,2,2)
    x = np.asarray(range(1,len(x2)+1))/float(len(x2))
    pyplot.plot(x,x2,color=pyplot.cm.hot(H_i*30),lw=2)
    pyplot.ylim([0,1])
    pyplot.xticks(x)
    pyplot.title('Tang traj.')    
    
pyplot.savefig(filename=(fig_dir + "beh_fig_summ.png"))
    
pyplot.close()
