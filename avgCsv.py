import csv
import DataProcessing
import sys

cw = csv.writer(file('ProtocolAvg.csv', 'w'))
prot_column = DataProcessing.allProtName()
prot_column.insert(0, "ProtocolAvg")
cw.writerow(prot_column)

print DataProcessing.avg_dict

"""
for net, res in DataProcessing.avg_dict.items():
	li = []
	li.append(net)
	for k in res :
		ind = prot_column.index(k["_id"])
		li.insert(ind,k["avgbyprot"])
	cw.writerow(li)

"""

