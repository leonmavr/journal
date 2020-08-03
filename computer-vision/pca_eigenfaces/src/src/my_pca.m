function [loads, scores, evals] = my_pca(X)
	n = size(X, 1);
	C = eye(n) - 1/n*ones(n,1)*ones(n,1)';
	X = C*X;
	S = X'*X;
	[loads, evals] = eigs(S);
	scores = [];
	for l=loads
		scores = [scores, X*l];
	end
end
