clc
clear all
close all


fe_Nr = '98';
choke_mode = 'CM';

sss = 131;
f_CFS    = zeros(sss,1);
I_eddy_S1   = zeros(sss,1);
I_disp_S1   = zeros(sss,1);
I_eddy_S2   = zeros(sss,1);
I_disp_S2   = zeros(sss,1);

asd = [];
for idx = 1:length(f_CFS)
    try
    file_id = [fe_Nr,'/',choke_mode,'/history/choke_',choke_mode,'_',fe_Nr,'_f_',num2str(idx-1),'-displacementCurrent-surfRegion-S_bar_1_in.hist'];
    [f_CFS(idx), I_disp_S1(idx)] = I_from_CFS(file_id);
    file_id = [fe_Nr,'/',choke_mode,'/history/choke_',choke_mode,'_',fe_Nr,'_f_',num2str(idx-1),'-displacementCurrent-surfRegion-S_bar_2_in.hist'];
    [f_CFS(idx), I_disp_S2(idx)] = I_from_CFS(file_id);

    file_id = [fe_Nr,'/',choke_mode,'/history/choke_',choke_mode,'_',fe_Nr,'_f_',num2str(idx-1),'-magEddyCurrent-surfRegion-S_bar_1_in.hist'];
    [f_CFS(idx), I_eddy_S1(idx)] = I_from_CFS(file_id);
    file_id = [fe_Nr,'/',choke_mode,'/history/choke_',choke_mode,'_',fe_Nr,'_f_',num2str(idx-1),'-magEddyCurrent-surfRegion-S_bar_2_in.hist'];
    [f_CFS(idx), I_eddy_S2(idx)] = I_from_CFS(file_id);
    catch 
        asd = [asd idx];
    end
end
f_CFS(asd) = [];
I_eddy_S1(asd) = [];
I_disp_S1(asd) = [];
I_eddy_S2(asd) = [];
I_disp_S2(asd) = [];

if strcmp(choke_mode,'CM')
    Z_CFS = 1./(I_eddy_S1+I_disp_S1+I_eddy_S2+I_disp_S2);
else
    Z_CFS = 2./(I_eddy_S1+I_disp_S1);
end
Z_CFS = real(Z_CFS) - 1j*imag(Z_CFS);


% Extract CST simulation data using LF solver
[f_CST, Z_CST_Re, Z_CST_Im, Z_CST_abs] = Z_CST_LF([fe_Nr,'/Z_choke_LF_',fe_Nr,'_',choke_mode,'_ReIm.txt']);
Z_CST = Z_CST_Re + 1j*Z_CST_Im;

% Extract CST simulation data using HF solver
Z_data = readmatrix([fe_Nr,'/Z_choke_HF_',fe_Nr,'_',choke_mode,'_ReIm.txt']);
if strcmp(fe_Nr,'N37')
    f_CST_HF = Z_data(1:1059,1);
    Z_CST_HF = Z_data(1:1059,2) + 1j*Z_data(1062:end,2);
else
    f_CST_HF = Z_data(1:1001,1);
    Z_CST_HF = Z_data(1:1001,2) + 1j*Z_data(1004:end,2);
end





%% Extract RLC parameter

f_start = 1e4;
f_end = 1e8;

f_meas = f_CFS([f_CFS>=f_start & f_CFS <= f_end]);
Z_meas = Z_CFS([f_CFS>=f_start & f_CFS <= f_end]);


Fs = 1./Z_meas;
s = 1j*2*pi*f_meas;
m = 5;
n = m-1;
Ns = length(s);

N_max = 10;
N_iter = 0;
eps_iter = 100;
eps_max = 0.1;


Np = n;

[bn, an] = RFA(Fs,s,n,m);

Fsfit = zeros(size(s));
while eps_iter>eps_max && N_iter<N_max
    [Ks,Rs,Ps,an,bn] = IRFA2(Fs,s,bn,an);
    unstables=real(Ps)>0;  
    if ~isempty(unstables)
      Ps(unstables)=Ps(unstables)-1.1*real(Ps(unstables)); %Forcing unstable poles to be stable
    end

    [bn,an] = residue(Rs,Ps,Ks);
    bn = bn';
    an = an';

    Fsfit = s.^(m:-1:0)*bn./(s.^(n:-1:0)*an);
    
    eVF = abs(Fs - Fsfit)./abs(Fs); % Deviation
    eps_iter = max(eVF);
    N_iter = N_iter + 1;
end


% [R,L,Rr,Lr,Cr,Rc1,Rc2,Lc1,Lc2,Cc1,Cc2] = Extract_element_extan(bn,an);
[R,C,Rr,Lr,Cr,Rc1,Rc2,Lc,Cc] = Extract_element_Ys(bn,an);


f_fit = logspace(-2,10,5000)';
s = 1j*2*pi*f_fit;


% 
Y_fit = R + s*C;
qweqwe = 0;
for idx = 1:length(Rr)
    if Cr(idx) == 0 && Rr(idx) ~= 0
        Y_fit = Y_fit + 1./(Rr(idx)+s*Lr(idx));
    elseif Lr(idx) == 0 && Rr(idx) ~= 0
        Y_fit = Y_fit + s*Cr(idx)./(1+s*Cr(idx)*Rr(idx)) - 1/Rr(idx);
    end
end

for idx = 1:length(Cc)
    if Lc(idx) ~= 0
        Y_fit = Y_fit + 1./(s*Lc(idx) + Rc1(idx) + Rc2(idx)./(1+s*Cc(idx)*Rc2(idx)));
    end
end

I = find([f_CFS>=f_start & f_CFS <= f_end]);
idx = [I([1,4]);I(ceil(linspace(9,length(I),10)));I(end)];


% impedance plot
figure(4)
loglog(f_CFS([f_CFS>=f_start & f_CFS <= f_end]),abs(Z_CFS([f_CFS>=f_start & f_CFS <= f_end])),'-ok','LineWidth',2,'MarkerIndices',2:10:100,'MarkerSize',10)
hold on
loglog(f_CST([f_CST>=f_start & f_CST <= f_end]),abs(Z_CST([f_CST>=f_start & f_CST <= f_end])),'--m','LineWidth',2)
loglog(f_CST_HF([f_CST_HF>=f_start & f_CST_HF <= f_end]),abs(Z_CST_HF([f_CST_HF>=f_start & f_CST_HF <= f_end])),'-.r','LineWidth',2)
loglog(f_fit([f_fit>=f_start & f_fit <= f_end]),abs(1./Y_fit([f_fit>=f_start & f_fit <= f_end])),':b','LineWidth',3)
hold off
grid on
legend('openCFS','CST LF', 'CST HF', 'EC','Location','northwest')
xlabel('Frequency [Hz]')
ylabel('Impedance Magnitude [\Omega]')
set(gca,'FontSize',18)
title('Fair-Rite 98 (CM)')




% Passivity test
all(Y_fit+conj(Y_fit)>0)

figure (5)
loglog(f_fit,real(Y_fit),'LineWidth',2)
hold on
grid on
xlabel('Frequency [Hz]')
ylabel('Admittance Real [\Omega]')
set(gca,'FontSize',18)
title('Fair-Rite 98 (CM)')

