%rng('default')
% spectral clustring based on MATLAB guide
%sim_value = 0.2;
%Estimate the number of clusters using the similarity graph and perform spectral clustering on the similarity matrix.
%Find the distance between each pair of observations in X by using the pdist and squareform functions with the default Euclidean distance metric.
%input_table = table;
%dist_temp = pdist(input_table);
%dist = squareform(dist_temp);
%dist = table;
%dist_original_table = original_table;
%dist(dist<0.4) = 0;
%dist_original_table(dist_original_table<0.4) = 0;
%sim_value= 0.95;
%Construct the similarity matrix from the pairwise distance and confirm that the similarity matrix is symmetric.
%S = exp(-dist.^2);
%issymmetric(S);
%Limit the similarity values to 0.5 so that the similarity graph connects only points whose pairwise distances are smaller than the search radius.
%S_eps = S;
%S_eps(S_eps<sim_value) = 0;

%Create a graph object from S.
%G_eps = graph(S_eps);
%Visualize the similarity graph.
%figure(1)
%plot(G_eps)
%cluster_list= unique(conncomp(G_eps));
%kx = max(cluster_list);

%[idx3, V] = spectralcluster(S_eps,k,'Distance','precomputed');
[idx3, V] = spectralcluster(S,k,'Distance','precomputed');
%figure(2)
%gscatter(dist(:,1),dist(:,2),idx3);
%plot(graph(S));

%tabulate(idx3)
[clusters, I] = sort(idx3); 
clusters= [clusters I];
clearvars I;

%Best_spectre_8_by_8
%Best_spectre_10_by_10
%Best_spectre_12_by_12
%Best_spectre_14_by_14

best_cluster_script

clearvars c9 c10 c11 cl1 cl2 cl3 cl4 cl5 cl6 c1_size c2_size c3_size c4_size c5_size c6_size x best_matrix stan_cluster1 stan_cluster2 stan_cluster3 stan_cluster4 stan_cluster5 stan_cluster6;
