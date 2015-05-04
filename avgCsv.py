import csv
import DataProcessing
import sys

prot_dict = {}

cw = csv.writer(file(sys.argv[1]+'.csv', 'w'))
colt_row = DataProcessing.allColtName()
for i in DataProcessing.allProtName():
	prot_dict[i] = [i]
colt_row.insert(0, sys.argv[1])
cw.writerow(colt_row)


for net, res in DataProcessing.avg_dict.items():
	ind = colt_row.index(net)
	map(lambda x: prot_dict[x["_id"]].insert(ind,x["avgbyprot"]), res)

map(lambda (k,v): cw.writerow(v), prot_dict.items())


"""
// this function is removed 
// It will be used if the col and row is changed
for net, res in DataProcessing.avg_dict.items():
	li = []
	li.append(net)
	for k in res :
		ind = prot_column.index(k["_id"])
		li.insert(ind,k["avgbyprot"])
	cw.writerow(li)

"""

