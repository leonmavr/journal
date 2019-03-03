A = im2double(imread('cameraman.bmp'));
[m, n] = size(A);
ranks = [1 2 10 20 round(1/4 * m*n/(m+n+1)) round(1/2 * m*n/(m+n+1))];
cd 'output';
fname = fopen('svd_results.txt','w');
fprintf(fname,'rank, number of elements required, compression ratio, norm2(A-A_k), sigma_(k+1)\n');
for r = ranks
    [U,S,V] = svd(A);
    A_k = U(:,1:r) * S(1:r, 1:r) * V(:, 1:r)';
    % numbers required to stores the approximation
    % size of U + no non-zero singular values + size of V
    numbers_req = numel(U(:,1:r)) + nnz(S(1:r, 1:r)) + numel(V(:,1:r));
    figure,imshow(A_k);
    imwrite(A_k,strcat('rank',int2str(r),'.bmp'));
    % for norm 2 we could do max(max(abs(A - A_k))
    fprintf(fname,strcat(int2str(r),',',int2str(numbers_req),',',...
        num2str((m*r + r + r*n)/(m*n)), ',',num2str(norm(A-A_k,2)), ','...
        , num2str(S(r+1,r+1)), '\n'));
end
fclose(fname);
close all; cd '..';
