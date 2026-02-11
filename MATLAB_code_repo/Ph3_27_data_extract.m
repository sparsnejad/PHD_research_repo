
clc

input_file= p103ph38A89S3sorted;
p103ph38A89S3_data = [];
p103ph38A89S3_table = [];

%labels= {'base', 'comp', 'p101_r1', 'p101_r2', 'p101_r3', 'p102_r1', 'p102_r2', 'p102_r3', 'p103_r1', 'p103_r2', 'p103_r3', 'p104_r1', 'p104_r2', 'p104_r3', 'p105_r1', 'p105_r2', 'p105_r3'};
% temp_data= [base_comp p101_r1 p101_r2 p101_r3 p102_r1 p102_r2 p102_r3 p103_r1 p103_r2 p103_r3 p104_r1 p104_r2 p104_r3 p105_r1 p105_r2 p105_r3];
temp_data= [labels input_file];
%mean_data= all_data;

mean_data= [ 
    mean(temp_data(1:2,:));
         temp_data(3:7,:); 
    mean(temp_data(8:9,:));
         temp_data(10:13,:);
    mean(temp_data(14:15,:));
         temp_data(16:18,:);
    mean(temp_data(19:20,:));
         temp_data(21:22,:);
    mean(temp_data(23:24,:));
         temp_data(25:25,:);
    mean(temp_data(26:27,:)); 
         
    
         ];
     
s = 6;     
table_rep = zeros(s,s);
r= 1;
c= 1;
for n = 1:21
    table_rep(r,c)= mean_data(n,3);
    table_rep(c,r)= mean_data(n,3);
    c= c+1;
    if(c > s)
        r= r+1;
        c= r;
    end
        
end    

p103ph38A89S3_data= mean_data;
p103ph38A89S3_table= table_rep;

clearvars mean_data table_rep r c temp_data all_data input_file temp n s;