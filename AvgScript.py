from pymongo import MongoClient
import sys
import GlobalDirEnviron
import csv
import Gnuplot
import glob

client = MongoClient('localhost', 27017)
db_name = client.Bonafide
Csv_Dir = "../"+GlobalDirEnviron.Csv_Result_Dir+"/"
Chart_Path = "../"+ GlobalDirEnviron.Chart_Result_Dir+"/"
# Find all the Network Type except Null
allNetwork_list = db_name['DocByUsertoken'].distinct("Network", { "Network" : { "$nin" : [""] }})
# Find all Provider Type except Null
allProvider_list = db_name['DocByUsertoken'].distinct("Provider", { "Provider" : { "$nin" : [""] }})
# Find all the protocol_specification_name
allProtocol_list = db_name['DocByUsertoken'].distinct("measurement_results.protocol_specification_name")

eval_criterion = ["latency", "download_protocol_bandwidth", "upload_protocol_bandwidth", "download_random_bandwidth", "upload_random_bandwidth"]

def agvCommand(yaxis):
	# Firstly, avg cal is done for every usertoken-protocol
	# Secondly, avg cal is done for all the usertoken-avg result
	# Result will show each protocol's avg value 
	return [
	{"$group": 
		{ "_id": {"user_token": "$user_token", "prot_name": "$protocol_specification_name"},
		  "avgbyuser": {"$avg":  "$"+yaxis}}},
	{ "$group": 
		{ "_id" : "$_id.prot_name",
		  "avgbyprot": {"$avg":  "$avgbyuser"}}},
	{"$project": 
		{"_id":1,
		"avgbyprot": 1}}]

def avgDict(comparison_criterion ,ev_criterion):
	avg_dict = {}
	# return the average dictionary
	for colt_name in comparison_criterion:
		print comparison_criterion
		avg_dict[colt_name]=list(db_name[colt_name].aggregate(agvCommand(ev_criterion)))
	return avg_dict


def makeCsv(comparison_criterion, comparison_name, ev_criterion):
	# make Csv file 
	prot_dict = {}
	fname =  "../"+GlobalDirEnviron.Csv_Result_Dir+"/"+comparison_name+"_"+ev_criterion+'.csv'
	cw = csv.writer(file(fname, 'w'))
	colt_row = list(comparison_criterion)
	# initializing dictionary to fill the result
	for i in allProtocol_list:
		prot_dict[i] = [i]*(len(colt_row)+1)
	colt_row.insert(0, ev_criterion)
	# write first row 
	# ex> [ latency, LGT, SKT, KT... last 3 column is changed by comparison_criterion]
	cw.writerow(colt_row)

	for col, res in avgDict(comparison_criterion, ev_criterion).items():
		# find the index of the col
		ind = colt_row.index(col)
		# fill the dictionary with result
		for i in res:
			prot_dict[i["_id"]][ind]=i["avgbyprot"]

    # write to CSV
	map(lambda (k,v): cw.writerow(v), prot_dict.items())


def makeChart(comparison_name, ev_criterion):
	chartname = Csv_Dir+comparison_name+"_"+ev_criterion+'.csv'
	graphname = chartname.split("/")[-1].strip(".csv")
	chartpng = Chart_Path+graphname+".png"

	g = Gnuplot.Gnuplot()
	g.title(graphname)
	g.xlabel('Protocolname')
	g.ylabel(graphname)
	#g('set palette defined ( 1  "#0025ad", 2  "#0042ad", 3  "#0060ad", 4  "#007cad", 5  "#0099ad",')
	#g('set palette defined ( 6  "#00ada4", 7  "#00ad88", 8  "#00ad6b", 9  "#007cad", 10  "#00ad4e",')
	g('fi = "#99ffff"')
	g('se = "#4671d5"')
	g('th = "#ff0000"')
	#g('fo = "#f36e00"')
	g('set term png')
	g('set output "%s"'%chartpng)
	g('set style data histogram')
	g('set style histogram cluster gap 1')
	g('set style fill solid 1.0 border -1')
	g('set datafile separator ","')
	g('set key autotitle columnhead')
	g('set auto x')
	g('set yrange[0:*]')
	plotcmd = "'"+str(chartname)+"'" + " using 2:xtic(1) ti col fc rgb fi"
	plotcmd += ", '' u 3 ti col fc rgb se"
	plotcmd += ", '' u 4 ti col fc rgb th"
	#plotcmd += ", '' u 5 ti col fc rgb fo"

	#plotcmd = "for [col=2:5] 'ProtocolAvg.csv' using col:xtic(1) ti col fc rgb fi"
	g.plot(plotcmd)


for i in eval_criterion:
	makeCsv(allProvider_list, "perProvider", i)
	makeChart("perProvider", i)
	makeCsv(allNetwork_list, "perNetwork", i)
	makeChart("perNetwork", i)


