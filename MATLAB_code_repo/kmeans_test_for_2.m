function [corners, C, sumd, D] = kmeans_test(table)
%KMEANS_TEST Summary of this function goes here
%   Detailed explanation goes here

[corners, C, sumd, D] = kmeans(table, 10, 'EmptyAction','error')
plot(table(corners==1,1),table(corners==1,2),'y.','MarkerSize',12)
hold on;
plot(table(corners==2,1),table(corners==2,2),'m.','MarkerSize',12)
plot(table(corners==3,1),table(corners==3,2),'c.','MarkerSize',12)
plot(table(corners==4,1),table(corners==4,2),'r.','MarkerSize',12)
plot(table(corners==5,1),table(corners==5,2),'g.','MarkerSize',12)
plot(table(corners==6,1),table(corners==6,2),'b.','MarkerSize',12)
plot(table(corners==7,1),table(corners==7,2),'k.','MarkerSize',12)
plot(table(corners==8,1),table(corners==8,2),'y.','MarkerSize',12)
plot(table(corners==9,1),table(corners==9,2),'m.','MarkerSize',12)
plot(table(corners==10,1),table(corners==10,2),'c.','MarkerSize',12)

end

