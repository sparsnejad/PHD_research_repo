% spectral clustring based on MATLAB guide
%sim_value = 0.2;
%Estimate the number of clusters using the similarity graph and perform spectral clustering on the similarity matrix.
%Find the distance between each pair of observations in X by using the pdist and squareform functions with the default Euclidean distance metric.
input_table = table
dist_temp = pdist(input_table);
dist = squareform(dist_temp);
%Construct the similarity matrix from the pairwise distance and confirm that the similarity matrix is symmetric.
S = exp(-dist.^2);
issymmetric(S)
%Limit the similarity values to 0.5 so that the similarity graph connects only points whose pairwise distances are smaller than the search radius.
S_eps = S;
S_eps(S_eps<sim_value) = 0;

%Create a graph object from S.
G_eps = graph(S_eps);
%Visualize the similarity graph.
figure(1)
plot(G_eps)
cluster_list= unique(conncomp(G_eps))
k = max(cluster_list)
idx3 = spectralcluster(S_eps,k,'Distance','precomputed');
figure(2)
gscatter(input_table(:,1),input_table(:,2),idx3);


