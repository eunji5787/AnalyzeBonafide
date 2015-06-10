from pymongo import MongoClient
import sys

client = MongoClient('localhost', 27017)
db_name = client.Bonafide

def selectCollection(colt_name):
	# select the collection
	return db_name[colt_name]

def upsertDoc(colt_name, user_token, protocol_specification_name, js_dict):
	# Using upsert function to avoid duplicate usertoken-protocol being inserted	
	# The first usertoken-protocol dict will only be inserted
	colt_name.update({
		"user_token": user_token,
		"protocol_specification_name":protocol_specification_name},
		js_dict,
		True)

def substituteNullString(st):
	# if user does not submit network name - others
	if len(st) == 0:
		return "NoneInput"
	else:
		return st

def createNetworkcollection(nw_dict):
	# Each test is stored as one document into collection
	# Collection is decided by each json file's Network type 
	# ex) 3G, LTE, LTE-A, 3_Band_LTE
	stname = nw_dict["Student Name"]
	stnum = nw_dict["Student Number"]
	dataplan = nw_dict["Dataplan"]
	network = substituteNullString(nw_dict["Network"])
	provider =  substituteNullString(nw_dict["Provider"])
	m_result = nw_dict["measurement_results"]

	for i in m_result:
		i['Dataplan'] = dataplan
		i['Provider'] = provider
		i['Network'] = network
		i["Student Name"] = stname
		i["Student Number"] = stnum
		#insertDoc(selectCollection(network), i)		
		upsertDoc(
			selectCollection(network), i["user_token"], i["protocol_specification_name"], i)

# main function
map(lambda x: createNetworkcollection(x), db_name['DocByUsertoken'].find())

"""
not used anymore

def insertDoc(colt_name, js_dict):
	# insert command is substituted by update command
	# insert each doc in a selected collection
	colt_name.insert(js_dict)

def allNetworkType():
	# not used anymore
	# Find all the Network Type except Null
	return db_name['DocByUsertoken'].distinct("Network", { "Network" : { "$nin" : [""] }})
"""
