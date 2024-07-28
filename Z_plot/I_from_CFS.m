function [f_CFS, current_lad] = I_from_CFS(id_file)
%I_from_CFS Extract the current and its frequency of the openCFS simulation
% from text file 
%   INPUT: id_file is the file name
%   OUTPUT: f_CFS is the frequency
%           current_lad is the current at frequency f_CFS

    opts = detectImportOptions(id_file,'FileType','text');
    result_disp = readmatrix(id_file,opts);
    
    temp1 = str2num(result_disp{3});
    f_CFS = temp1(1);
    I_disp = temp1(2);
    phi_disp = temp1(3);

    current_lad = I_disp .* exp(1j * deg2rad(phi_disp));
end