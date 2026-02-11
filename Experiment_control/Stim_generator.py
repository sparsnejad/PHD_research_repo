################################
#This file creates a 12 parter electrotactile csv script for human trials
################################

import math
import csv
import funcs
import random


################################
BF= 1 #Beat frequency
BDC= 50 #Beat duty Cycle
PBD= 2000 #Post-bundle delay
TF= 80 #texture frequency
TDC= 10 #texture duty cycle
PuF= 2000 #Base pulse frequency

################################
#file1_title= 'demo - 120ms.csv'
file1_title= 'demo - 120ms - for labels.csv'

################################
rand_seed = 2
################################
out_tile=       'ph3.9_seed2.csv'
label_tile=     'ph3.9_seed2_labels.csv'
out_tile_1_1=   'ph3.9_S2Pt1.1.csv'
out_tile_1_2=   'ph3.9_S2Pt1.2.csv'
out_tile_2_1=   'ph3.9_S2Pt2.1.csv'
out_tile_2_2=   'ph3.9_S2Pt2.2.csv'
out_tile_3_1=   'ph3.9_S2Pt3.1.csv'
out_tile_3_2=   'ph3.9_S2Pt3.2.csv'
out_tile_4_1=   'ph3.9_S2Pt4.1.csv'
out_tile_4_2=   'ph3.9_S2Pt4.2.csv'
out_tile_5_1=   'ph3.9_S2Pt5.1.csv'
out_tile_5_2=   'ph3.9_S2Pt5.2.csv'
out_tile_6_1=   'ph3.9_S2Pt6.1.csv'
out_tile_6_2=   'ph3.9_S2Pt6.2.csv'

with open(file1_title) as csv_file:
    raw_list = csv.reader(csv_file, delimiter=',')
    scramble_list_1 = []
    for row in raw_list:
        if row[0] != 'number':
            scramble_list_1 += [row]
        print(row)
    print('ok')

Archtypes= []
Archtypes+= ['HEADER']
Archtypes+= [scramble_list_1[0:4]]
Archtypes+= [scramble_list_1[4:12]]
Archtypes+= [scramble_list_1[12:16]]
Archtypes+= [scramble_list_1[16:21]]
Archtypes+= [scramble_list_1[21:24]]
Archtypes+= [[scramble_list_1[24]]]
Archtypes+= [scramble_list_1[25:29]]
Archtypes+= [scramble_list_1[29:31]]

Archtypes[1].insert(0, 'archtype1')
Archtypes[2].insert(0, 'archtype2')
Archtypes[3].insert(0, 'archtype3')
Archtypes[4].insert(0, 'archtype4')
Archtypes[5].insert(0, 'archtype5')
Archtypes[6].insert(0, 'archtype6')
Archtypes[7].insert(0, 'archtype7')
Archtypes[8].insert(0, 'archtype8')


temp_list = []
only_comp_list= []
label_list =[]
tempx=[]
tempy=[]
counter = 1

for x in range(1, len(Archtypes)):
    for y in range(1, len(Archtypes[x])):
        temp= [][:]
        tempx=Archtypes[x][y][:]
        tempy=Archtypes[x][y][:]
        tempx[1]= 'base'
        tempy[1]= 'base'
        temp.append(tempx[:])
        temp.append(tempy[:])
        temp.append(Archtypes[x][y][:])
        for loop in range(5):
            temp_list.append(temp[:])
            label_list.append([temp[0][0], temp[1][0]])

 
for Archy1 in range(1, len(Archtypes)-1):
    for Archy2 in range(Archy1 +1, len(Archtypes)):
        for x in range(1, len(Archtypes[Archy1])):
            for y in range(1, len(Archtypes[Archy2])):
                #print('printing the boys')
                #print(Archtypes[Archy1][x][:])
                #print(Archtypes[Archy2][y][:])
                coin = random.randint(1, 2)
                if coin == 1:
                    #print(scramble_list[x])
                    #print(scramble_list[y])
                    temp= [][:]
                    tempx=Archtypes[Archy1][x][:]
                    tempy=Archtypes[Archy2][y][:]
                    tempx[1]= 'base'
                    tempy[1]= 'base'
                    temp.append(tempx[:])
                    temp.append(tempy[:])
                    temp.append(Archtypes[Archy1][x][:])
                    temp_list.append(temp[:])
                    only_comp_list.append(temp[:])
                    #print(temp[:])
                    label_list.append([temp[0][0], temp[1][0]])
                    #print('True')
                elif coin == 2:
                    temp= [][:]
                    tempx=Archtypes[Archy1][x][:]
                    tempy=Archtypes[Archy2][y][:]
                    tempx[1]= 'base'
                    tempy[1]= 'base'
                    temp.append(tempy[:])
                    temp.append(tempx[:])
                    temp.append(Archtypes[Archy2][y][:])
                    temp_list.append(temp[:])
                    only_comp_list.append(temp[:])
                    #print(temp[:])
                    label_list.append([temp[1][0], temp[0][0]])
                    #print('False')

random.seed(1)
subset_of_temp_list= random.sample(temp_list, 10)

with open('global_10_subsets.csv', mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (subset_of_temp_list):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])

#print(temp_list)
random.seed(rand_seed)
random.shuffle (temp_list)          
random.seed(rand_seed)
random.shuffle (label_list)          
#counter=1
        
with open(out_tile, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])
        
         
with open(label_tile, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['base', 'comp'])
    for row in (label_list):
         stim_writer.writerow(row)

with open(out_tile_1_1, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[0:47]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])
with open(out_tile_1_2, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[47:94]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])

with open(out_tile_2_1, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[94:141]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])
with open(out_tile_2_2, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[141:188]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])

with open(out_tile_3_1, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[188:235]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])
with open(out_tile_3_2, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[235:282]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])

with open(out_tile_4_1, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[282:329]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])
with open(out_tile_4_2, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[329:376]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])         
         
with open(out_tile_5_1, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[376:423]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])
with open(out_tile_5_2, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[423:470]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])
         
with open(out_tile_6_1, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[470:517]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])
with open(out_tile_6_2, mode='w', newline='') as csv_file:
    stim_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    stim_writer.writerow(['number', 'sequence', 'stack', 'BF' , 'TF', 'BDC', 'TDC', 'length'])
    for row in (temp_list[517:561]):
         stim_writer.writerow(row[0])
         stim_writer.writerow(row[1])
         stim_writer.writerow(row[2])