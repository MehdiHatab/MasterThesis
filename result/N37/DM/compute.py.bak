#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 06:04:17 2020

@author: klaus
"""


#import matplotlib.pylab as plt
#import scipy.integrate
import numpy as np
from sys import exit
from subprocess import call
#import glob



def I_from_CFS(file_lad):
    f_CFS, current_lad, phase_lad = np.loadtxt(file_lad, skiprows=3, unpack=True)
    current_lad = current_lad*np.exp(np.deg2rad(phase_lad)*1j)

    return f_CFS,current_lad

#f,mu_re = np.loadtxt('mu_75_Re.txt',skiprows=36,unpack=True)
#f,mu_im = np.loadtxt('mu_75_Im.txt',skiprows=36,unpack=True)

f,mu_re,mu_im = np.loadtxt('mu_N37_CFS.txt',unpack=True)

xml_file = 'choke_CM_freq.xml'

for ll in range(len(f)):
    line = 90
    infile = open('mat.xml', 'r+')
    content = infile.readlines()
    content[line] = f"            <real> 1.2566E-06 *{mu_re[ll]}</real>\n"
    content[line+1] = f"            <imag> 1.2566E-06 *{mu_im[ll]}</imag>\n"
    infile.close
    infile = open('mat.xml', 'w') #clears content of file. 
    infile.close
    infile = open('mat.xml', 'r+')
    for item in content: #rewrites file content from list 
        infile.write("%s" % item)
    infile.close()


    line = 61
    infile = open(xml_file, 'r+')
    content = infile.readlines()
    content[line] = f'					<freq value="{f[ll]}" />\n'
    infile.close
    infile = open(xml_file, 'w') #clears content of file. 
    infile.close
    infile = open(xml_file, 'r+')
    for item in content: #rewrites file content from list 
        infile.write("%s" % item)
    infile.close()
    call('/mnt/c/Users/lk/Devel/CFS_BIN/build_opt/bin/cfs -t10 -p {0} choke_CM_N37_f_{1}'.format(xml_file,ll),shell=True)



# f_CFS_CM = []
# I_CFS_CM_disp1 = []
# I_CFS_CM_eddy1 = []
# I_CFS_CM_disp2 = []
# I_CFS_CM_eddy2 = []
# for ll in range(1049):
#     if ll == 336 or ll == 358:
#         print('%d \n',ll)
#     else:
#         file_lad = f"choke_T37_opencfs2/history/choke_CM_T37_f_{ll}-displacementCurrent-surfRegion-S_bar_1_in.hist"
#         temp1,temp2 = I_from_CFS(file_lad)
#         f_CFS_CM.append(temp1)
#         I_CFS_CM_disp1.append(temp2)
#         file_lad = f"choke_T37_opencfs2/history/choke_CM_T37_f_{ll}-displacementCurrent-surfRegion-S_bar_2_in.hist"
#         temp1,temp2 = I_from_CFS(file_lad)
#         I_CFS_CM_disp2.append(temp2)
#         file_lad = f"choke_T37_opencfs2/history/choke_CM_T37_f_{ll}-magEddyCurrent-surfRegion-S_bar_1_in.hist"
#         temp1,temp3 = I_from_CFS(file_lad)
#         I_CFS_CM_eddy1.append(temp3)
#         file_lad = f"choke_T37_opencfs2/history/choke_CM_T37_f_{ll}-magEddyCurrent-surfRegion-S_bar_2_in.hist"
#         temp1,temp3 = I_from_CFS(file_lad)
#         I_CFS_CM_eddy2.append(temp3)



# infile = open('asd.xml', 'r+')
# for item in content: #rewrites file content from list 
#     infile.write("%s" % item)
# infile.close()