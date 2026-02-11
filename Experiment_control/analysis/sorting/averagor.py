

import math
import pandas



d1 = pandas.read_csv('101 pre c2 r1_Organized.csv')
d2 = pandas.read_csv('101 pre c2 r2_Organized.csv')
d3 = pandas.read_csv('101 pre c2 r3_Organized.csv')

#print (d1.iloc[:,[0]])

result= pandas.concat([d1, d2, d3]).groupby(level=0).mean()
#result.iloc[:,[0]]= d1.iloc[:,[0]]
print(result)

result.to_csv("101 pre c2 average.csv")

