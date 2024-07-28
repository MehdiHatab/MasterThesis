function [bn, an] = RFA(Fs,s,n,m)

A = [s.^(m:-1:0), -Fs.*s.^(n:-1:1)];

Ar = real(A);  % Real part of matrix A
Ai = imag(A);  % Imaginary part of matrix A
br = real(Fs); % Real part of vector B
bi = imag(Fs); % Imaginary part of vector B


An = [Ar;Ai];
Bn = [br;bi];
[Xmax Ymax] = size(Ar);
[Q,R2] = qr(An,0); % QR decomposition - Matrix Q and R of An
At = R2;           % It updates the matrix An
B = Q.'*Bn;        % It updates the vector Bn
for col = 1:Ymax
     Euclidian(col) = norm(At(:,col),2); % Euclidian norm
     At(:,col) = At(:,col)./Euclidian(col);
end
x = At\B; % Solution for the system (Ax = b)
x = x./Euclidian.'; % Real solution

% H = 2*An'*An;
% c = -2*Bn'*An;
% x = quadprog(H,c);

bn = x(1:m+1);
an = [x(m+2:end);1];