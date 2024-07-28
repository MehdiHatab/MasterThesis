function [Ks,Rs,Ps,an,bn] = IRFA2(Fs,s,bn,an)

n = length(an)-1;
m = length(bn)-1;

D_s = s.^(n:-1:0)*an;
N_s = s.^(m:-1:0)*bn;

M = [s.^(m:-1:0), -Fs.*s.^(n:-1:1)];

W1 = diag(1./(real(N_s./D_s)));
W2 = diag(1./(imag(N_s./D_s)));
Sigma = diag(1./D_s);


A_real = real(W1*Sigma*M);
A_imag = imag(W2*Sigma*M);
An = [];
Bn = [];
Euclidian = [];
[Xmax Ymax] = size(A_real); % Size for matrix A
Ar = A_real;                % Real part of matrix A
Ai = A_imag;                % Imaginary part of matrix A
br = real(W1*Sigma*Fs);     % Real part of vector B
bi = imag(W2*Sigma*Fs);     % Imaginary part of vector B

An = [Ar;Ai];
Bn = [br;bi];

[Q,R2] = qr(An,0); % QR decomposition - Matrix Q and R of An
At = R2;           % It updates the matrix An
B = Q.'*Bn;        % It updates the vector Bn
for col = 1:Ymax
     Euclidian(col) = norm(At(:,col),2); % Euclidian norm
     At(:,col) = At(:,col)./Euclidian(col);
end
x = At\B;           % Solution for the system (Ax = b)
x = x./Euclidian.'; % Real solution


bn = x(1:m+1);
an = [x(m+2:end); 1];
[Rs,Ps,Ks] = residue(bn,an);

    