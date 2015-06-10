from pymongo import MongoClient
import sys


client = MongoClient('localhost', 27017)
db_name = client.Bonafide
avg_dict = {}


def allProtName():
	# Find all the protocol_specification_name
	return db_name['DocByUsertoken'].distinct("measurement_results.protocol_specification_name")

def allNetworkType():
	# Find all the Network Type except Null
	return db_name['DocByUsertoken'].distinct("Network", { "Network" : { "$nin" : [""] }})

def allProvider():
	# Find all Provider Type except Null
	return db_name['DocByUsertoken'].distinct("Provider", { "Provider" : { "$nin" : [""] }})

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


# main process
if len(sys.argv) == 1:
  print "Input the yaxis label"
else:
	yaxis = sys.argv[1]
	for colt_name in allNetworkType():
	# For testing provider csv
	#for colt_name in allProvider():
		avg_dict[colt_name]=list(db_name[colt_name].aggregate(agvCommand(yaxis)))

