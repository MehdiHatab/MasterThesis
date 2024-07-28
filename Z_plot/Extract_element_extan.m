function [R,L,Rr,Lr,Cr,Rc1,Rc2,Lc1,Lc2,Cc1,Cc2] = Extract_element_extan(bn,an)
[Rs,Ps,Ks] = residue(bn,an);

if ~isempty(Ks)
    try
        R = Ks(2);
        L = Ks(1);
    catch
        R = Ks(1);
        L = 0;
    end
else
    R = 0;
    L = 0;
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
            Rr(idx) = Rs_real(idx)/Ps_real(idx);
            Lr(idx) = -Rr(idx)/Ps_real(idx);
        else
            Rr(idx) = -Rs_real(idx)/Ps_real(idx);
            Cr(idx) = 1 /Rs_real(idx);
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
    Lc1 = zeros(aa,1);
    Cc1 = zeros(aa,1);
    Rc2 = zeros(aa,1);
    Lc2 = zeros(aa,1);
    Cc2 = zeros(aa,1);

    s = tf('s');
    for idx = 1:length(Ps_compl)
        Z = Rs_compl(idx)/(s-Ps_compl(idx)) + conj(Rs_compl(idx))/(s-conj(Ps_compl(idx)));
        num = Z.Numerator{1};
        den = Z.Denominator{1};
        a = num(2); 
        b = num(3); 
        m = den(2); 
        n = den(3); 

        Rc1(idx) = b/n;
        Lc1(idx) = Rc1(idx)/m;
        Cc1(idx) = 1/(Lc1(idx)*n);
        Cc2(idx) = 1/(a-1/Cc1(idx));
        Lc2(idx) = 1/(n*Cc2(idx));
        Rc2(idx) = 1/(m*Cc2(idx));
    end

else
    Rc1 = 0;
    Rc2 = 0;
    Lc1 = 0;
    Lc2 = 0;
    Cc1 = 0;
    Cc2 = 0;
end





