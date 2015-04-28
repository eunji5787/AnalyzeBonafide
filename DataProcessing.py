from pymongo import MongoClient
import json
import sys
import Gnuplot
import numpy as np
import sys

client = MongoClient('localhost', 27017)
db_name = client.Bonafide

def calAvg(avg_list):

	return 

def allProtName():

	return db_name['DocByUsertoken'].distinct("measurement_results.protocol_specification_name")

def allColtName():

	return db_name['DocByUsertoken'].distinct("Network", { "Network" : { "$nin" : [""] }})

def agvCommand(prot_name, yaxis):

	return [ 
	{"$match": 
		{ 
		"protocol_specification_name": prot_name}}, 
	{"$group": 
		{ "_id": "$user_token", 
		  "avgbyuser": {"$avg":  "$"+yaxis}}},
	{ "$group": 
		{ "_id" : "null",
		  "avgbyprot": {"$avg":  "$avgbyuser"}}},
	{"$project": 
		{"_id":0,
		"avgbyprot": 1}}, explain:True]


for colt_name in allColtName():
	for prot_name in allProtName():
		print prot_name +":"+colt_name
		print list(db_name[colt_name].aggregate(agvCommand(prot_name,"download_protocol_bandwidth")))


#print list(db_name['3G'].aggregate(pipeline=agvCommand("SIP", "download_protocol_bandwidth","download_total_bytes" )))

#prot_name = raw_input("Name protocol..Bit")