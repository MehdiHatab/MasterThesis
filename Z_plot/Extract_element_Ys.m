function [R,C,Rr,Lr,Cr,Rc1,Rc2,Lc,Cc] = Extract_element_Ys(bn,an)
[Rs,Ps,Ks] = residue(bn,an);

if ~isempty(Ks)
    try
        R = Ks(2);
        C = Ks(1);
    catch
        R = Ks(1);
        C = 0;
    end
else
    R = 0;
    C = 0;
end

R_idx = [];
C_idx = [];
Ps_real = [];
Ps_compl = [];
Rs_real = [];
Rs_compl = [];
NR = 0;
NC = 0;
for idx = 1:length(Ps)
    if isreal(Ps(idx))
        NR = NR + 1;
        R_idx = [R_idx,idx];
        Ps_real = [Ps_real; Ps(idx)];
        Rs_real = [Rs_real; Rs(idx)];
    else
        NC = NC + 1;
        C_idx = [C_idx,idx];
        Ps_compl = [Ps_compl; Ps(idx)];
        Rs_compl = [Rs_compl; Rs(idx)];
    end
end

if ~isempty(Ps_compl)
    Ps_compl = Ps_compl(1:2:end);
%     Ps_compl = real(Ps_compl) + 1j*abs(imag(Ps_compl));
    Rs_compl = Rs_compl(1:2:end);
%     Rs_compl = real(Rs_compl) + 1j*abs(imag(Rs_compl));
    NC = NC/2;
end

if ~isempty(Ps_real)
    m = length(Rs_real);

    Rr = zeros(m,1);
    Lr = zeros(m,1);
    Cr = zeros(m,1);

    for idx = 1:m
        if Rs_real(idx) < 0
            Rr(idx) = Ps_real(idx)/Rs_real(idx);
            Cr(idx) = -1 /Ps_real(idx)/Rr(idx);
        else
            Rr(idx) = -Ps_real(idx)/Rs_real(idx);
            Lr(idx) = 1 /Rs_real(idx);
        end
    end
else
    Rr = 0;
    Lr = 0;
    Cr = 0;
end


if ~isempty(Ps_compl)
    aa = length(Ps_compl);
    Rc1 = zeros(aa,1);
    Lc  = zeros(aa,1);
    Cc  = zeros(aa,1);
    Rc2 = zeros(aa,1);

    for idx = 1:length(Ps_compl)
        % Numerator coefficients 
        num = [0, Rs_compl(idx)+conj(Rs_compl(idx)), (-conj(Rs_compl(idx))*Ps_compl(idx))-Rs_compl(idx)*conj(Ps_compl(idx))];
        % Denominator coefficients
        den = [1, (-Ps_compl(idx) - conj(Ps_compl(idx))), Ps_compl(idx)*conj(Ps_compl(idx))];
        a = num(2); 
        b = num(3); 
        m = den(2); 
        n = den(3);
        
        Lc(idx) = 1/a;
        Rc1(idx) = Lc(idx)*m - Lc(idx)^2*b;
        Rc2(idx) = n/b - Rc1(idx);
        Cc(idx) = 1/(b*Lc(idx)*Rc2(idx));
    end

else
    Rc1 = 0;
    Rc2 = 0;
    Lc = 0;
    Cc = 0;
end





