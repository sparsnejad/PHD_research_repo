function [corners, C, sumd, D] = kmeans_test(table)
%KMEANS_TEST Summary of this function goes here
%   Detailed explanation goes here

[corners, C, sumd, D] = kmeans(table, 3, 'EmptyAction','error')
plot(table(corners==1,1),table(corners==1,2),'b.','MarkerSize',12)
hold on;
plot(table(corners==2,1),table(corners==2,2),'g.','MarkerSize',12)
plot(table(corners==3,1),table(corners==3,2),'r.','MarkerSize',12)


end

