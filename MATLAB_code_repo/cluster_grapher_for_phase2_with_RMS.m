% similar to k-fold cross validation
clc

table= original_table;
table_size = size(table,1);
table(1:(table_size+1):end) = 0;

dist = table;
dist_original_table = original_table;

dist_original_table(1:(table_size+1):end) = 0;
dist_original_table(dist_original_table<0.4) = 0;

sim_value= 0.5;
S = exp(-dist.^2);
%S = exp(-dist_original_table.^2);
issymmetric(S);
S_eps = S;
S_eps(S_eps<sim_value) = 0;
%Create a graph object from S.
G_eps = graph(S_eps);
%Visualize the similarity graph.
figure(1)
plot(G_eps)
cluster_list= unique(conncomp(G_eps));
