import pandas

csv_file = pandas.read_csv('S4 P129, P130, P123.csv', skiprows = 2)
for col in csv_file.columns: 
    print(col) 
#sorted_csv = csv_file.sort_values(by=['base BF', 'base', 'comp'], ascending = (True, True, True))
sorted_csv = csv_file.sort_values(by=['base', 'comp'], ascending = (True, True))
sorted_csv.to_csv("S4 P129, P130, P123_sorted.csv")

