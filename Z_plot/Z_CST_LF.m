function [f_CST, Z_CST_Re, Z_CST_Im, Z_CST_abs] = Z_CST_LF(id_file)
%Z_CST_LF Extract the impedance and its frequency of the CST simulation
% from text file 
%   INPUT: id_file is the file name
%   OUTPUT: f_CST is the frequency
%           Z_CST_Re is the real part of the impedance at frequency f_CST
%           Z_CST_Im is the imaginary part of the impedance at frequency f_CST
%           Z_CST_abs is the absolute value of the impedance at the frequency f_CST

    infile = fopen(id_file, 'r+');
    content = textscan(infile, '%s', 'Delimiter', '\n');
    content = content{1};
    fclose(infile);

    temp1 = {};
    temp2 = {};
    for item = 11:8:length(content) % rewrites file content from list
        temp1{end+1} = content{item};
    end
    for item = 15:8:length(content) % rewrites file content from list
        temp2{end+1} = content{item};
    end
    

    for idx = 1:numel(temp1)
        data1(idx,:) = str2num(temp1{idx});
        data2(idx,:) = str2num(temp2{idx});
    end

    
    f_CST = data1(:, 1);
    Z_CST_Re = data1(:, 2);
    Z_CST_Im = data2(:, 2);
    
    Z_CST_abs = sqrt(Z_CST_Re.^2 + Z_CST_Im.^2);
end

