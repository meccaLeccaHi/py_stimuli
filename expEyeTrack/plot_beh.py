# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:17:50 2017

@author: root
"""

import numpy as np
#import matplotlib.pyplot as plt
#import plotly.plotly as py
from matplotlib import pyplot

def plot_beh(STEP_LIST, TRAJ_LIST, CORRECT,rad_only = False, SCORE = 0):
    
#    np.asarray(f_names)[np.where(STEP_LIST>3)]
#    np.asarray(correct)[np.where(STEP_LIST>3)]
    
#    temp_correct = np.asarray(CORRECT)
#    temp_correct[temp_correct==''] = None
    
    if SCORE==0:
        barCol = 'blue'
    elif SCORE<=25:
        barCol = 'red'
    elif SCORE <=50:
        barCol = 'yellow'
    else:
        barCol = 'green'
    
    foo = np.asarray(CORRECT)[np.where(STEP_LIST>3)]
    if any(foo>=0):
        rad_results = [np.mean(foo[foo>=0])]
        for i in range(4):
            foo = np.asarray(CORRECT)[np.where((TRAJ_LIST==1)&(STEP_LIST==i))]
            rad_results.append(np.mean(foo[foo>=0]))
    else:
        rad_results = []
         
#    np.asarray(f_names)[np.where((TRAJ_LIST==2)&(STEP_LIST==i))]
    tan_results = []
    for i in range(3):
        foo = np.asarray(CORRECT)[np.where((TRAJ_LIST==2)&(STEP_LIST==0))]
        if any(foo>=0):
            # tan_results.append(np.mean(map(int, foo[foo!=None])))
            tan_results.append(np.mean(foo[foo>=0]))
    
    foo = np.asarray(CORRECT)[np.where((TRAJ_LIST==1)&(STEP_LIST==3))]
    if any(foo>=0):
        tan_results.append(np.mean(foo[foo>=0]))
    
    x1 = np.asarray(rad_results)*100
    x2 = np.asarray(tan_results)*100
    
#    pyplot.clf()
    if rad_only:
        plot_num = 1
    else:
        plot_num = 2
    
    #define plot size in inches (width, height) & resolution(DPI)
    
    
    if rad_only:
        pyplot.figure(figsize=(4.5, 4.5), dpi=100)
    else:
        pyplot.figure(figsize=(6, 4), dpi=100)
    

    ax1 = pyplot.subplot(1,plot_num,1,axisbg='k')
    x = np.asarray(range(len(x1)))/((len(x1)-1.0)/100)
    pyplot.plot(x,np.tile(25.0,(1,len(x1)))[0],'--',color='grey',lw=2)
    if SCORE!=0:
       pyplot.plot(x,np.tile(int(SCORE),(1,len(x1)))[0],'--',color=barCol,lw=3.5) 
    pyplot.plot(x,x1,color='blue',lw=4)
    pyplot.ylim([0,100])
    pyplot.xticks(x)
    pyplot.xlabel('% disguised')
    pyplot.ylabel('% correct')
    if rad_only==False:
        pyplot.title('Radial traj.')
    
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_linewidth(0.5)
    ax1.spines['left'].set_linewidth(0.5)
    ax1.spines['bottom'].set_color('white')
    ax1.spines['left'].set_color('white')
    ax1.title.set_color('white')
    ax1.yaxis.label.set_color('white')
    ax1.xaxis.label.set_color('white')
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')
    
    if rad_only==False:
            
        ax2 = pyplot.subplot(1,plot_num,2,axisbg='k')
        x = np.asarray(range(1,len(x2)+1))/((len(x2)/100.0))
        pyplot.plot(x,np.tile(25.0,(1,len(x2)))[0],'--',color='grey',lw=2)
        if SCORE!=0:
            pyplot.plot(x,np.tile(int(SCORE),(1,len(x1)))[0],'--',color=barCol,lw=3.5)        
        pyplot.plot(x,x2,color='blue',lw=4)
        pyplot.ylim([0,100])
        pyplot.xticks(x)
        pyplot.xlabel('% disguised')
        pyplot.title('Tang traj.')
    
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['bottom'].set_linewidth(0.5)
        ax2.spines['left'].set_linewidth(0.5)
        ax2.spines['bottom'].set_color('white')
        ax2.spines['left'].set_color('white')
        ax2.title.set_color('white')
        ax2.yaxis.label.set_color('white')
        ax2.xaxis.label.set_color('white')
        ax2.tick_params(axis='x', colors='white')
        ax2.tick_params(axis='y', colors='white')   
    
    return pyplot


