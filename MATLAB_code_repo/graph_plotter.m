% similar to k-fold cross validation
%clc

%Nodes= {'A1.1' 'A1.4' 'A1.6' 'A1.8' 'A2.1' 'A2.4' 'A2.5' 'A2.6' 'A2.7' 'A2.9' 'A2.10' 'A2.16' 'A3.1' 'A3.2' 'A3.3' 'A3.6' 'A3.9' 'A4.3' 'A4.4' 'A4.9' 'A4.10' 'A4.11' 'A5.1' 'A5.3' 'A5.4' 'A7.2' 'A7.3' 'A7.4' 'A7.8' 'A8.1' 'A8.2' };
Nodes= { 'A1.1' 'A1.6' 'A1.8' 'A2.1' 'A2.5' 'A2.6' 'A2.7' 'A2.9' 'A2.10' 'A2.16' 'A3.1' 'A3.3' 'A3.6' 'A3.9' 'A4.3' 'A4.4' 'A4.9' 'A4.10' 'A4.11' 'A5.3' 'A5.4'	'A7.2' 'A7.8' 'A8.2' };


dist = data;

for i= 1:24
    %dist(i,i)= 1-dist(i,i)
    dist(i,i)= 1;
end

sim_value= 0.5;
S = exp(-dist.^2);

S_eps = S;
S_eps(S_eps<sim_value) = 0;

%Create a graph object from S.
G_eps = graph(S_eps, Nodes);
%Visualize the similarity graph.
figure(1)
plot(G_eps)
cluster_list= unique(conncomp(G_eps));
kx = max(cluster_list);

