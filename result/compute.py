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
import subprocess
#import glob
import os

os.chdir("N37/DM2/")
subprocess.Popen("compute.py 1", shell=True)
os.chdir("../../75/DM2")
os.system("compute.py 1")
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