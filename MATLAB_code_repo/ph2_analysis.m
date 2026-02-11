
clc
clear
filename = 'Z:\research\aha\Projects\electrotactile_stimulation\Trials\2020 trials\phase_2_Trials\analysis\statistics\p119 s6_sorted.csv';
delimiter = ',';
startRow = 2;
formatSpec = '%*s%*s%f%*s%*s%*s%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
fclose(fileID);

p119s6_sorted = [dataArray{1:end-1}];

formatSpec = '%*s%*s%*s%*s%f%f%[^\n\r]';
fileID = fopen(filename,'r');
dataArray = textscan(fileID, formatSpec, 'Delimiter', delimiter, 'HeaderLines' ,startRow-1, 'ReturnOnError', false, 'EndOfLine', '\r\n');
fclose(fileID);

ph2_labels = [dataArray{1:end-1}];

clearvars filename delimiter startRow formatSpec fileID dataArray ans;

input_file= p119s6_sorted;
p119s6_data = [];
p119s6_table = [];

%labels= {'base', 'comp', 'p101_r1', 'p101_r2', 'p101_r3', 'p102_r1', 'p102_r2', 'p102_r3', 'p103_r1', 'p103_r2', 'p103_r3', 'p104_r1', 'p104_r2', 'p104_r3', 'p105_r1', 'p105_r2', 'p105_r3'};
% temp_data= [base_comp p101_r1 p101_r2 p101_r3 p102_r1 p102_r2 p102_r3 p103_r1 p103_r2 p103_r3 p104_r1 p104_r2 p104_r3 p105_r1 p105_r2 p105_r3];
temp_data= [ph2_labels input_file];
%mean_data= all_data;

mean_data= [ 
    mean(temp_data(1:3,:));
         temp_data(4:25,:); 
    mean(temp_data(26:28,:));
         temp_data(29:49,:);
    mean(temp_data(50:52,:));
         temp_data(53:72,:);
    mean(temp_data(73:75,:));
         temp_data(76:94,:);
    mean(temp_data(95:97,:));
         temp_data(98:115,:);
    mean(temp_data(116:118,:)); 
         temp_data(119:135,:);
    mean(temp_data(136:138,:));
         temp_data(139:154,:);
    mean(temp_data(155:157,:));
         temp_data(158:172,:);
    mean(temp_data(173:175,:));
         temp_data(176:189,:);
    mean(temp_data(190:192,:));
         temp_data(193:205,:);
    mean(temp_data(206:208,:));
         temp_data(209:220,:);
    mean(temp_data(221:223,:));
         temp_data(224:234,:);
    mean(temp_data(235:237,:));
         temp_data(238:247,:);
    mean(temp_data(248:250,:));
         temp_data(251:259,:);
    mean(temp_data(260:262,:));
         temp_data(263:270,:);
    mean(temp_data(271:273,:));
         temp_data(274:280,:);
    mean(temp_data(281:283,:));
         temp_data(284:289,:);
    mean(temp_data(290:292,:));
         temp_data(293:297,:);
    mean(temp_data(298:300,:));
         temp_data(301:304,:);
    mean(temp_data(305:307,:));
         temp_data(308:310,:);
    mean(temp_data(311:313,:));
         temp_data(314:315,:);
    mean(temp_data(316:318,:));
         temp_data(319,:);
    mean(temp_data(320:322,:));
         ];
     
table_rep = zeros(23,23);
r= 1;
c= 1;
for n = 1:276
    table_rep(r,c)= mean_data(n,3);
    table_rep(c,r)= mean_data(n,3);
    c= c+1;
    if(c > 23)
        r= r+1;
        c= r;
    end
        
end   

p119s6_data= mean_data;
p119s6_table= table_rep;

clearvars mean_data table_rep r c temp_data all_data input_file temp n;