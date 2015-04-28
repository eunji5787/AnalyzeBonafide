from collections import Counter
from pymongo import MongoClient
import json
import sys

client = MongoClient('localhost', 27017)
db_name = client.Bonafide

def selectCollection(colt_name):
	# select the collection
	return db_name[colt_name]

def insertDoc(colt_name, js_dict):
	# insert each doc in a selected collection
	colt_name.insert(js_dict)

def NumofProtocol(m_result):
	# count the number of each protocols being tested
	protocol_list = map(lambda x : m_result[x]["protocol_specification_name"], range(len(m_result)))
	return dict(Counter(protocol_list))

def stuInfoLog(stname, stnum, network, protocol_dict):
	# insert the student's information and tested protocols information into StudentInfoLog collection
	if len(network) == 0:
		network = "NoneInput"
	protocol_dict["stname"] = stname
	protocol_dict["stnum"] = stnum
	protocol_dict["network"] = network
	insertDoc(selectCollection("StudentInfoLog"), protocol_dict)

def loadJson(filename):
	# load json file
	with open(filename, 'r') as f:
		js_dict =  json.loads(f.read())
	return js_dict

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
	network = js_dict["Network"]
	m_result = js_dict["measurement_results"]

	stuInfoLog(stname, stnum, network, NumofProtocol(m_result))

	for i in m_result:
		i['Dataplan'] = dataplan
		i['Network'] = network
		insertDoc(selectCollection(network), i)

if sys.argv[0] == "":
	print "input valid json file name"
else:
	js_dict = loadJson(sys.argv[1])
	docByUsertoken(js_dict)
	docByProtocol(js_dict)

