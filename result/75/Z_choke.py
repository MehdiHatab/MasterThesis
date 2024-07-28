# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 00:36:39 2023

@author: Mehdi
"""



import matplotlib.pylab as plt
import numpy as np



def I_from_CFS(file_lad):
    f_CFS, current_lad, phase_lad = np.loadtxt(file_lad, skiprows=3, unpack=True)
    current_lad = current_lad*np.exp(np.deg2rad(phase_lad)*1j)

    return f_CFS,current_lad



def Z_CST_LF(id_file):
    infile = open(id_file, 'r+')
    content = infile.readlines()
    infile.close()
    
    
    temp1 = []
    temp2 = []
    for item in range(10,len(content),8): 
        temp1.append(content[item])
    for item in range(14,len(content),8): 
        temp2.append(content[item])
        
    f_CST, Z_CST_Re = np.loadtxt(temp1, unpack=True)
    f_CST, Z_CST_Im = np.loadtxt(temp2, unpack=True)
    Z_CST_abs = np.sqrt(Z_CST_Re**2 + Z_CST_Im**2)
    return f_CST,Z_CST_Re,Z_CST_Im,Z_CST_abs


def Z_choke_HF(id_file):
    infile = open(id_file, 'r+')
    content = infile.readlines()
    infile.close()


    steps = int((len(content)-3*32)/32)

    temp1 = []
    for ll in range(32):
        if ll==0:
            for item in range(2,steps+2,1):
                temp1.append(content[item])
        else:
            for item in range(ll*(steps+3)+2,ll*(steps+3)+2+steps,1):
                temp1.append(content[item])
                
    f, SS = np.loadtxt(temp1, unpack=True)
    f = f[0:steps]
    S = []
    for ll in range(16):
        S.append(SS[(2*ll)*steps:(2*ll+1)*steps] + 1j*SS[(2*ll+1)*steps:(2*ll+2)*steps])
        

    SSS = np.zeros( (steps, 4,4),dtype=complex )

    for ll in range(steps):
        SSS[ll] = np.array([[S[0][ll],S[4][ll],S[8][ll],S[12][ll]],
                            [S[1][ll],S[5][ll],S[9][ll],S[13][ll]],
                            [S[2][ll],S[6][ll],S[10][ll],S[14][ll]],
                            [S[3][ll],S[7][ll],S[11][ll],S[15][ll]]])
     

    M = np.array([[1,-1,0,0],[1,1,0,0],[0,0,1,-1],[0,0,1,1]])/np.sqrt(2)


    # S_m = M*SSS*np.linalg.inv(M)
    S_m = (M @ SSS) @ np.linalg.inv(M)
    Z_CM = 25 * ((1 + S_m[:, 1, 1]) * (1 + S_m[:, 3, 3]) - S_m[:, 3, 1] * S_m[:, 1, 3]) / (2 * S_m[:, 3, 1])
    Z_DM = 100 * ((1 + S_m[:, 0, 0]) * (1 + S_m[:, 2, 2]) - S_m[:, 2, 0] * S_m[:, 0, 2]) / (2 * S_m[:, 2, 0])
        
    return f,Z_CM,Z_DM
        



file_lad = 'Z_75_CM_2ports_ReIm.txt' 
f_CST_75,Z_CST_75_CM_Re,Z_CST_75_CM_Im,Z_CST_75_CM_abs = Z_CST_LF(file_lad)
# f_CFS_CM = []
# I_CFS_CM_disp1 = []
# I_CFS_CM_eddy1 = []
# I_CFS_CM_disp2 = []
# I_CFS_CM_eddy2 = []
# for ll in range(1049):
#     if not(ll == 336 or ll == 358):
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
# I_CFS_CM_eddy1 = np.array(I_CFS_CM_eddy1) 
# I_CFS_CM_disp1 = np.array(I_CFS_CM_disp1)
# I_CFS_CM_eddy2 = np.array(I_CFS_CM_eddy2) 
# I_CFS_CM_disp2 = np.array(I_CFS_CM_disp2)
# I_CFS_CM = I_CFS_CM_disp1+I_CFS_CM_eddy1 + I_CFS_CM_disp2+I_CFS_CM_eddy2
# Z_CFS_CM = 1.0/(I_CFS_CM)



f_CFS_75_CM = []
I_CFS_75_CM_disp1 = []
I_CFS_75_CM_eddy1 = []
I_CFS_75_CM_disp2 = []
I_CFS_75_CM_eddy2 = []
for ll in range(120):
    try:
        file_lad = f"history/choke_CM_75_grading2_f_{ll}-displacementCurrent-surfRegion-S_bar_1_in.hist"
        temp1,temp2 = I_from_CFS(file_lad)
        f_CFS_75_CM.append(temp1)
        I_CFS_75_CM_disp1.append(temp2)
        file_lad = f"history/choke_CM_75_grading2_f_{ll}-displacementCurrent-surfRegion-S_bar_2_in.hist"
        temp1,temp2 = I_from_CFS(file_lad)
        I_CFS_75_CM_disp2.append(temp2)
        file_lad = f"history/choke_CM_75_grading2_f_{ll}-magEddyCurrent-surfRegion-S_bar_1_in.hist"
        temp1,temp3 = I_from_CFS(file_lad)
        I_CFS_75_CM_eddy1.append(temp3)
        file_lad = f"history/choke_CM_75_grading2_f_{ll}-magEddyCurrent-surfRegion-S_bar_2_in.hist"
        temp1,temp3 = I_from_CFS(file_lad)
        I_CFS_75_CM_eddy2.append(temp3)
    except :
        print(ll)
I_CFS_75_CM_eddy1 = np.array(I_CFS_75_CM_eddy1) 
I_CFS_75_CM_disp1 = np.array(I_CFS_75_CM_disp1)
I_CFS_75_CM_eddy2 = np.array(I_CFS_75_CM_eddy2) 
I_CFS_75_CM_disp2 = np.array(I_CFS_75_CM_disp2)
I_CFS_75_CM = I_CFS_75_CM_disp1+I_CFS_75_CM_eddy1 + I_CFS_75_CM_disp2+I_CFS_75_CM_eddy2
Z_CFS_75_CM = 1.0/(I_CFS_75_CM_disp1+I_CFS_75_CM_eddy1)/2



f_CFS_75_DM = []
I_CFS_75_DM_disp1 = []
I_CFS_75_DM_eddy1 = []
I_CFS_75_DM_disp2 = []
I_CFS_75_DM_eddy2 = []
for ll in range(120):
    try:
        file_lad = f"history/choke_DM_75_grading2_f_{ll}-displacementCurrent-surfRegion-S_bar_1_in.hist"
        temp1,temp2 = I_from_CFS(file_lad)
        f_CFS_75_DM.append(temp1)
        I_CFS_75_DM_disp1.append(temp2)
        file_lad = f"history/choke_DM_75_grading2_f_{ll}-displacementCurrent-surfRegion-S_bar_2_in.hist"
        temp1,temp2 = I_from_CFS(file_lad)
        I_CFS_75_DM_disp2.append(temp2)
        file_lad = f"history/choke_DM_75_grading2_f_{ll}-magEddyCurrent-surfRegion-S_bar_1_in.hist"
        temp1,temp3 = I_from_CFS(file_lad)
        I_CFS_75_DM_eddy1.append(temp3)
        file_lad = f"history/choke_DM_75_grading2_f_{ll}-magEddyCurrent-surfRegion-S_bar_2_in.hist"
        temp1,temp3 = I_from_CFS(file_lad)
        I_CFS_75_DM_eddy2.append(temp3)
    except :
        print(ll)
I_CFS_75_DM_eddy1 = np.array(I_CFS_75_DM_eddy1) 
I_CFS_75_DM_disp1 = np.array(I_CFS_75_DM_disp1)
I_CFS_75_DM_eddy2 = np.array(I_CFS_75_DM_eddy2) 
I_CFS_75_DM_disp2 = np.array(I_CFS_75_DM_disp2)
I_CFS_75_DM = I_CFS_75_DM_disp1+I_CFS_75_DM_eddy1 + I_CFS_75_DM_disp2+I_CFS_75_DM_eddy2
Z_CFS_75_DM = 2/(I_CFS_75_DM_disp1+I_CFS_75_DM_eddy1)




# 75 CM
plt.subplots()
plt.loglog(f_CST_75, np.abs(Z_CST_75_CM_abs))
# plt.loglog(f_EC_75_CM, np.abs(Z_EC_75_CM))
# plt.loglog(f_75_HF_open, np.abs(Z_75_CM_HF_open))
# plt.loglog(f_75_HF_E, np.abs(Z_75_CM_HF_E))
plt.loglog(f_CFS_75_CM, np.abs(Z_CFS_75_CM))
plt.grid(True)
plt.xlabel('Frequency in Hz')
plt.ylabel('Z in Ohm')
plt.legend(['75 CM CST','75 CM EC','75 CM HF open','75 CM HF E'])
plt.title('Absolute value')

# plt.subplots()
# plt.loglog(f_CST_75, np.abs(Z_CST_75_CM_Re))
# plt.loglog(f_CST_75, np.abs(np.real(Z_EC_CM_75)))
# plt.loglog(f_75_HF_open, np.abs(np.real(Z_75_CM_HF_open)))
# plt.loglog(f_75_HF_E, np.abs(np.real(Z_75_CM_HF_E)))
# plt.grid(True)
# plt.xlabel('Frequency in Hz')
# plt.ylabel('Z in Ohm')
# plt.legend(['75 CM CST','75 CM EC','75 CM HF open','75 CM HF E'])
# plt.title('Real value')

# plt.subplots()
# plt.loglog(f_CST_75, np.abs(Z_CST_75_CM_Re))
# plt.loglog(f_CST_75, np.abs(np.imag(Z_EC_CM_75)))
# plt.loglog(f_75_HF_open, np.abs(np.imag(Z_75_CM_HF_open)))
# plt.loglog(f_75_HF_E, np.abs(np.imag(Z_75_CM_HF_E)))
# plt.grid(True)
# plt.xlabel('Frequency in Hz')
# plt.ylabel('Z in Ohm')
# plt.legend(['75 CM CST','75 CM EC','75 CM HF open','75 CM HF E'])
# plt.title('Imaginary value')




plt.subplots()
# plt.loglog(f_CST_75, np.abs(Z_CST_75_CM_abs))
# plt.loglog(f_EC_75_CM, np.abs(Z_EC_75_CM))
# plt.loglog(f_75_HF_open, np.abs(Z_75_CM_HF_open))
# plt.loglog(f_75_HF_E, np.abs(Z_75_CM_HF_E))
plt.loglog(f_CFS_75_DM, np.abs(Z_CFS_75_DM))
plt.grid(True)
plt.xlabel('Frequency in Hz')
plt.ylabel('Z in Ohm')
plt.legend(['75 CM CST','75 CM EC','75 CM HF open','75 CM HF E'])
plt.title('Absolute value')

plt.show()



# T37 DM



# 75 DM


































