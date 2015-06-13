import GlobalDirEnviron
import csv
import QueryAvg
import sys

prot_dict = {}
fname =  "../"+GlobalDirEnviron.Csv_Result_Dir+"/"+sys.argv[1]+'.csv'
cw = csv.writer(file(fname, 'w'))
colt_row = QueryAvg.allProvider()
# For testing csv Provider
# colt_row = QueryAvg.allProvider()
for i in QueryAvg.allProtName():
	prot_dict[i] = [i]*(len(colt_row)+1)
colt_row.insert(0, sys.argv[1])
cw.writerow(colt_row)

for net, res in QueryAvg.avg_dict.items():
	ind = colt_row.index(net)
	# lambda cannot do the assignment function
	for i in res:
		prot_dict[i["_id"]][ind]=i["avgbyprot"]

map(lambda (k,v): cw.writerow(v), prot_dict.items())


"""
// this function is removed 
// It will be used if the col and row is changed
for net, res in QueryAvg.avg_dict.items():
	li = []
	li.append(net)
	for k in res :
		ind = prot_column.index(k["_id"])
		li.insert(ind,k["avgbyprot"])
	cw.writerow(li)

"""

