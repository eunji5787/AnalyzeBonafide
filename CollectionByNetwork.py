import GlobalDirEnviron
from collections import Counter
from pymongo import MongoClient
import json
import sys
import glob
import JsonFormatter

client = MongoClient('localhost', 27017)
db_name = client.Bonafide

def selectCollection(colt_name):
	# select the collection
	return db_name[colt_name]

def insertDoc(colt_name, js_dict):
	# insert each doc in a selected collection
	colt_name.insert(js_dict)

def networkNotNull(network):
	# if user does not submit network name - others
	if len(network) == 0:
		return "NoneInput"
	else:
		return network

def numofProtocol(m_result):
	# count the number of each protocols being tested
	protocol_list = map(lambda x : m_result[x]["protocol_specification_name"], range(len(m_result)))
	return dict(Counter(protocol_list))

def stuInfoLog(stname, stnum, network, protocol_dict):
	# insert the student's information and tested protocols information into StudentInfoLog collection

	protocol_dict["stname"] = stname
	protocol_dict["stnum"] = stnum
	protocol_dict["network"] = network
	insertDoc(selectCollection("StudentInfoLog"), protocol_dict)

def loadJson(filename):
	# load json file
	with open(filename, 'r') as f:
		js_dict =  json.loads(f.read())
	if db_name["DocByUsertoken"].find({"user_token": js_dict["user_token"]}).count() == 0:
		return JsonFormatter.strToInt(js_dict)

def docByUsertoken(js_dict):
	# insert into DocByUsertoken collection, each json file (one user token) is stored as one document
	insertDoc(selectCollection("DocByUsertoken"), js_dict)

def docByProtocol(js_dict):
	# Each test is stored as one document into collection
	# Collection is decided by each json file's Network type 
	# ex) 3G, LTE, LTE-A, 3_Band_LTE
	stname = js_dict["Student Name"]
	stnum = js_dict["Student Number"]
	dataplan = js_dict["Dataplan"]
	network = networkNotNull(js_dict["Network"])
	m_result = js_dict["measurement_results"]

	stuInfoLog(stname, stnum, network, numofProtocol(m_result))

	for i in m_result:
		i['Dataplan'] = dataplan
		i['Network'] = network
		insertDoc(selectCollection(network), i)

def findJsonfilename():
	return glob.glob("../"+GlobalDirEnviron.Student_Data_Dir+"/*.json")


for i in map(lambda x: loadJson(x), findJsonfilename()):
	if i != None:
		# Bad.. Should be fixed
		docByUsertoken(i)
		docByProtocol(i)

