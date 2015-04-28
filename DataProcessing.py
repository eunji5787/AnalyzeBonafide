from pymongo import MongoClient
import json
import sys
import Gnuplot
import numpy as np

client = MongoClient('localhost', 27017)
db_name = client.Bonafide

#g = Gnuplot.Gnuplot(persist=1)

#colt_name = raw_input("Name one of those collections..3G/ LTE-A/ LTE/ 3_Band_LTE")

for i in db_name["3G"].find():
	print i["protocol_specification_name"]
	for k, v in i.items():
		if k.startswith("upload_") == True:
			print k +":"+ v
#prot_name = raw_input("Name protocol..Bit")