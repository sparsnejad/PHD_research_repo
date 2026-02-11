import pandas
import csv

csv_file = pandas.read_csv('p101 BDC r1_sorted.csv', skiprows = 0)
row_count = csv_file.shape[0]-1
column_count = csv_file.shape[1]
# creating a list of dataframe columns 
columns = list(csv_file) 

sd_value = list()
base_value = list()
comp_value = list()

for i in columns: 
    x = 0
    if i == "S/D (Binary)":
        while x <= row_count:
            sd_value.append(csv_file[i][x]) 
            x += 1
    elif i == "base":
        while x <= row_count:
            base_value.append(csv_file[i][x]) 
            x += 1
    elif i == "comp":
        while x <= row_count:
            comp_value.append(csv_file[i][x]) 
            x += 1

base_to_sd_comp = list()
current_base_list = list()
old_base = 1

i = 0
while i < len(base_value):
    if (base_value[i] != old_base):
        base_to_sd_comp.append(current_base_list)
        current_base_list = list()
        old_base = base_value[i]

    
    sd_comp_tup = (sd_value[i], comp_value[i])
    current_base_list.append(sd_comp_tup)
    
    i += 1

base_to_sd_comp.append(current_base_list)
current_base_list = list()



final_base_list = list()

base_set = set(base_value)
cropped_base_list = list(base_set)

comp_set = set(comp_value)
cropped_comp_list = list(comp_set)

i = 0
average_sum = 0
average_count = 0
current_comp = 0
for base_list in base_to_sd_comp:
    base_super_list = list()
    comp_super_list = list()
    for tup in base_list:
        if tup[1] != cropped_base_list[i]:
            average = average_sum/average_count
            base_super_list.append(average)
            comp_super_list.append(current_comp)
            average_sum = 0
            average_count = 0
        average_sum += tup[0]
        average_count += 1 
        current_comp = tup[1]
        
    average = average_sum/average_count
    base_super_list.append(average)
    comp_super_list.append(current_comp)
    average_sum = 0
    average_count = 0

    
    final_base_list.append((base_super_list, comp_super_list))
    i += 1


base_i = 0
csv_row_list = list()
for tup in final_base_list:
    row_dict = {}
    row_dict[""] = cropped_base_list[base_i]
    base_i += 1
    
    averages = tup[0]
    comps = tup[1]
    i = 0
    
    while i < len(averages):
        row_dict[comps[i]] = averages[i]
        i += 1
    csv_row_list.append(row_dict)

csv_row_list.append({"": "base"})
#print(csv_row_list)





file = open('p101 BDC r1_organized.csv', 'w+', newline = '')
cropped_comp_list.append("comp")
cropped_comp_list = [""] + cropped_comp_list
#print(cropped_comp_list)


headers = cropped_comp_list
with file:

    write = csv.DictWriter(file, fieldnames = cropped_comp_list)
    write.writeheader()
    
    write.writerows(csv_row_list)
    
file.close()





        