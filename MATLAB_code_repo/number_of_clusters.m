% spectral clustring based on MATLAB guide
%sim_value = 0.2;
%Estimate the number of clusters using the similarity graph and perform spectral clustering on the similarity matrix.
%Find the distance between each pair of observations in X by using the pdist and squareform functions with the default Euclidean distance metric.
dist = table;
%Construct the similarity matrix from the pairwise distance and confirm that the similarity matrix is symmetric.
S = exp(-dist.^2);
issymmetric(S)
%Limit the similarity values to 0.5 so that the similarity graph connects only points whose pairwise distances are smaller than the search radius.
S_eps = S;
counter = 1;
X = [];
Y = [];
for n= 0.5:0.0001:1
    S_eps(S_eps<n) = 0;
    G_eps = graph(S_eps);
    cluster_list= unique(conncomp(G_eps));
    X(counter) = n;
    Y(counter) = max(cluster_list);
    counter = counter+1;

end   
plot(X,Y);
clearvars X Y S S_eps n G-eps counter dist cluster_list