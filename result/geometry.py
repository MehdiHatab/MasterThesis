#!python


import sys
import numpy as np
cubit_dir = '/share/programs/Trelis/Coreform-Cubit-2021.4/bin'
sys.path.append(cubit_dir)
import cubit

#cubit.init(['trelis', '-journalfile', 'test.jou'])
cubit.init(['trelis', '-nojournal'])
cubit.cmd(f'reset')
cubit.cmd(f'undo on')
# Graphical Display during Python
#cubit.cmd(f'graphics window create') # Create display
#cubit.cmd(f'graphics flush') # Refresh window
#cubit.cmd(f'mouse') # Allows interaction, with 'q' button escape interaction
n_xBus = 14
n_xAir = 8
n_xChoke = 6
n_xAirChoke = 6
n_xHsteg = 6

n_zBus = 8
n_zAir = 8
n_zChoke = 6
n_zMiddle = 6

n_yAir = 8
n_yChoke = 8

airGrading = 1.5
busGrading = 1.5

#%% Define variables

c_x = 43.2
c_y = 27.9
c_z = 9.5	

# holes in choke
h_x = 13.3
h_z = 5.4
h_steg = 8.1

# bus bars
b_x = 5
b_y = 100
b_z = 2

# air
a_x = 100
a_z = 100


cubit.cmd(f'brick x {c_x}  y {c_y}  z {c_z}')
cubit.cmd(f'brick x {h_x}  y {c_y}  z {h_z}')
cubit.cmd(f'move volume 2 x {h_x/2+h_steg/2} z {c_z/2-h_z/2}')
cubit.cmd('volume 2 copy reflect x')
cubit.cmd('subtract volume 2 3 from volume 1 keep')
cubit.cmd('delete volume 2 3 1')


cubit.cmd(f'brick x {b_x}  y {b_y}  z {b_z}')
cubit.cmd(f'move volume 5 x {h_steg/2+h_x/2} z {c_z/2}')
cubit.cmd('volume 5 copy reflect x')

cubit.cmd(f'volume 4 copy reflect origin 0 0 {c_z/2} direction 0 0 1')

cubit.cmd(f'move volume all z {-c_z/2}')

cubit.cmd(f'brick x {a_x}  y {b_y}  z {a_z}')
cubit.cmd('subtract volume all except volume 8 from volume 8 keep')
cubit.cmd('delete volume 8')


cubit.cmd(f'webcut volume all with yplane offset {c_y/2}')
cubit.cmd(f'webcut volume all with yplane offset {-c_y/2}')


cubit.cmd(f'webcut volume all with zplane offset {c_z}')
cubit.cmd(f'webcut volume all with zplane offset {-c_z}')
cubit.cmd(f'webcut volume all with zplane offset {h_z}')
cubit.cmd(f'webcut volume all with zplane offset {-h_z}')
cubit.cmd(f'webcut volume all with zplane offset {b_z/2}')
cubit.cmd(f'webcut volume all with zplane offset {-b_z/2}')
cubit.cmd(f'webcut volume all with zplane offset 0')

cubit.cmd(f'webcut volume all with xplane offset {-h_steg/2}')
cubit.cmd(f'webcut volume all with xplane offset {h_steg/2}')
cubit.cmd(f'webcut volume all with xplane offset {c_x/2-(c_x/2-h_steg/2-h_x)}')
cubit.cmd(f'webcut volume all with xplane offset {-c_x/2+(c_x/2-h_steg/2-h_x)}')
cubit.cmd(f'webcut volume all with xplane offset {c_x/2}')
cubit.cmd(f'webcut volume all with xplane offset {-c_x/2}')

cubit.cmd(f'webcut volume all with xplane offset {h_steg/2+h_x/2-b_x/2}')
cubit.cmd(f'webcut volume all with xplane offset {h_steg/2+h_x/2+b_x/2}')

cubit.cmd(f'webcut volume all with xplane offset {-h_steg/2-h_x/2+b_x/2}')
cubit.cmd(f'webcut volume all with xplane offset {-h_steg/2-h_x/2-b_x/2}')



cubit.cmd('imprint all')
cubit.cmd('merge all')




######################################
#### Blocks and Nodesets
#####################################
cubit.cmd('block 1 add volume all except volume 10 67 63 65 5 13 68 11 6 66 14 64 146 33 32 7 199 145 102 217 254 27 253 121 26 41 82 218 49 101 236 48 4 25 235 200 122 43 50 81 ')
cubit.cmd('block 1 name "V_air"')

cubit.cmd('block 2 add volume 10 67 63 65 5 13 ')
cubit.cmd('block 2 name "V_busbar_1"')

cubit.cmd('block 3 add volume 68 11 6 66 14 64 ')
cubit.cmd('block 3 name "V_busbar_2"')

cubit.cmd('block 4 add volume 146 33 32 7 199 145 102 217 254 27 253 121 26 41 82 218 49 101 236 48 4 25 235 200 122 43 50 81 ')
cubit.cmd('block 4 name "V_choke"')



cubit.cmd(f'nodeset 1 add surface all with z_coord>{a_z/2-1e-3}')
cubit.cmd(f'nodeset 1 add surface all with z_coord < { -a_z/2+1e-3 }')
cubit.cmd(f'nodeset 1 add surface all with x_coord>{a_x/2-1e-3}')
cubit.cmd(f'nodeset 1 add surface all with x_coord < { -a_x/2+1e-3}')
cubit.cmd(f'nodeset 1 add surface all with y_coord>{b_y/2-1e-3} except surface 586 593 576 584 566 574 556 564 ')
cubit.cmd(f'nodeset 1 add surface all with y_coord < { -b_y/2+1e-3} except surface 586 593 576 584 566 574 556 564 ')
cubit.cmd('nodeset 1 name "S_air"')

cubit.cmd('nodeset 2 add surface 586 593 ')
cubit.cmd('nodeset 2 name "S_bar_2_in"')
cubit.cmd('nodeset 3 add surface 576 584 ')
cubit.cmd('nodeset 3 name "S_bar_1_in"')
cubit.cmd('nodeset 4 add surface  566 574 ')
cubit.cmd('nodeset 4 name "S_bar_2_out"')
cubit.cmd('nodeset 5 add surface 556 564 ')
cubit.cmd('nodeset 5 name "S_bar_1_out"')




######################################
#### Mesh
######################################
cubit.cmd('delete mesh')

############## lines ##################
eps = 1e-5

# busbars height
cubit.cmd(f'curve with length<={b_x+eps} and length>={b_x-eps} interval {n_xBus} scheme dualbias factor {busGrading} {busGrading}')
cubit.cmd(f'mesh curve with length<={b_x+eps} and length>={b_x-eps}')

cubit.cmd(f'curve with length<={h_steg+eps} and length>={h_steg-eps} interval {n_xHsteg} scheme dualbias factor 1 1')
cubit.cmd(f'mesh curve with length<={h_steg+eps} and length>={h_steg-eps}')

cubit.cmd(f'curve with length<={(h_x-b_x)/2+eps} and length>={(h_x-b_x)/2-eps} interval {n_xAirChoke} scheme dualbias factor 1 1')
cubit.cmd(f'mesh curve with length<={(h_x-b_x)/2+eps} and length>={(h_x-b_x)/2-eps}')

cubit.cmd(f'curve with length<={(c_x-2*h_x-h_steg)/2+eps} and length>={(c_x-2*h_x-h_steg)/2-eps} interval {n_xChoke} scheme dualbias factor 1 1')
cubit.cmd(f'mesh curve with length<={(c_x-2*h_x-h_steg)/2+eps} and length>={(c_x-2*h_x-h_steg)/2-eps}')

cubit.cmd(f'curve with length<={(a_x-c_x)/2+eps} and length>={(a_x-c_x)/2-eps} interval {n_xAir} scheme bias factor {airGrading}')
cubit.cmd(f'curve with length<={(a_x-c_x)/2+eps} and length>={(a_x-c_x)/2-eps} orient sense location 0 0 0 ')
cubit.cmd(f'mesh curve with length<={(a_x-c_x)/2+eps} and length>={(a_x-c_x)/2-eps}')


cubit.cmd(f'curve with length<={b_z/2+eps} and length>={b_z/2-eps} interval {n_zBus} scheme bias factor {busGrading}')
cubit.cmd(f'curve with length<={b_z/2+eps} and length>={b_z/2-eps} orient sense location 0 0 0 opposite ')
cubit.cmd(f'mesh curve with length<={b_z/2+eps} and length>={b_z/2-eps}')

cubit.cmd(f'curve with length<={h_z-b_z/2+eps} and length>={h_z-b_z/2-eps} interval {n_zMiddle} scheme dualbias factor 1 1')
cubit.cmd(f'mesh curve with length<={h_z-b_z/2+eps} and length>={h_z-b_z/2-eps}')

cubit.cmd(f'curve with length<={c_z-h_z+eps} and length>={c_z-h_z-eps} interval {n_zChoke} scheme dualbias factor 1 1')
cubit.cmd(f'mesh curve with length<={c_z-h_z+eps} and length>={c_z-h_z-eps}')

cubit.cmd(f'curve with length<={(a_z-2*c_z)/2+eps} and length>={(a_z-2*c_z)/2-eps} interval {n_zAir} scheme bias factor {airGrading}')
cubit.cmd(f'curve with length<={(a_z-2*c_z)/2+eps} and length>={(a_z-2*c_z)/2-eps} orient sense location 0 0 0 ')
cubit.cmd(f'mesh curve with length<={(a_z-2*c_z)/2+eps} and length>={(a_z-2*c_z)/2-eps}')


cubit.cmd(f'curve with length<={c_y+eps} and length>={c_y-eps} interval {n_yChoke}')
cubit.cmd(f'mesh curve with length<={c_y+eps} and length>={c_y-eps}')

cubit.cmd(f'curve with length<={(b_y-c_y)/2+eps} and length>={(b_y-c_y)/2-eps} interval {n_yAir}')
cubit.cmd(f'mesh curve with length<={(b_y-c_y)/2+eps} and length>={(b_y-c_y)/2-eps}')

cubit.cmd('volume all scheme map')
cubit.cmd('volume all redistribute nodes off')
cubit.cmd('volume all autosmooth target off')
cubit.cmd('mesh volume all')



cubit.cmd('volume all scale 0.001')  # scale from mm to m
cubit.cmd('export ansys cdb "choke.cdb" overwrite')








#call('/home/hatab/Devel/CFS_BIN/build_opt/bin/cfs -t12 -p {0} choke_const_normal1_1{1}'.format(xml_file,ll),shell=True)


