
clc

input_file= p101ph38A9S3;
p101ph38A9S3_data = [];
p101ph38A9S3_table = [];

%labels= {'base', 'comp', 'p101_r1', 'p101_r2', 'p101_r3', 'p102_r1', 'p102_r2', 'p102_r3', 'p103_r1', 'p103_r2', 'p103_r3', 'p104_r1', 'p104_r2', 'p104_r3', 'p105_r1', 'p105_r2', 'p105_r3'};
% temp_data= [base_comp p101_r1 p101_r2 p101_r3 p102_r1 p102_r2 p102_r3 p103_r1 p103_r2 p103_r3 p104_r1 p104_r2 p104_r3 p105_r1 p105_r2 p105_r3];
temp_data= [labels input_file];
%mean_data= all_data;

mean_data= [ 
    mean(temp_data(1:2,:));
         temp_data(3:5,:); 
    mean(temp_data(6:7,:));
         temp_data(8:9,:);
    mean(temp_data(10:11,:));
         temp_data(12:12,:);
    mean(temp_data(13:14,:));
         
         ];
     
table_rep = zeros(4,4);
r= 1;
c= 1;
for n = 1:10
    table_rep(r,c)= mean_data(n,3);
    table_rep(c,r)= mean_data(n,3);
    c= c+1;
    if(c > 4)
        r= r+1;
        c= r;
    end
        
end   

p101ph38A9S3_data= mean_data;
p101ph38A9S3_table= table_rep;

clearvars mean_data table_rep r c temp_data all_data input_file temp n;