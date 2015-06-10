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
	# insert command is substituted by update command
	# insert each doc in a selected collection
	colt_name.insert(js_dict)

def upsertDoc(colt_name, user_token, js_dict):
	# update command to avoid duplicate user_token being inserted
	colt_name.update({"user_token": user_token},
		js_dict,
		True)

def numofProtocol(m_result):
	# count the number of each protocols being tested
	protocol_list = map(lambda x : m_result[x]["protocol_specification_name"], range(len(m_result)))
	return dict(Counter(protocol_list))

def substituteNullString(st):
	# if user does not submit network name - others
	if len(st) == 0:
		return "NoneInput"
	else:
		return st

def stuInfoLog(user_token, js_dict):
	st_dict = {}
	# insert the student's information and tested protocols information into StudentInfoLog collection
	st_dict["stname"] = js_dict["Student Name"]
	st_dict["stnum"] = js_dict["Student Number"]
	st_dict["user_token"] = user_token
	st_dict["dataplan"] = js_dict["Dataplan"]
	st_dict["network"] = substituteNullString(js_dict["Network"])
	st_dict["provider"] = substituteNullString(js_dict["Provider"])
	st_dict.update(numofProtocol(js_dict["measurement_results"]))
	upsertDoc(selectCollection("StudentInfoLog"), user_token, st_dict)

def docByUsertoken(user_token, js_dict):
	# insert into DocByUsertoken collection, each json file (one user token) is stored as one document
	# insertDoc(selectCollection("DocByUsertoken"), js_dict) - not used anymore 
	upsertDoc(selectCollection("DocByUsertoken"), user_token, js_dict)

def loadJson(filename):
	# load json file
	with open(filename, 'r') as f:
		js_dict =  json.loads(f.read())
	return JsonFormatter.strToInt(js_dict)

def findJsonfilename():
	return glob.glob("../"+GlobalDirEnviron.Student_Data_Dir+"/*.json")


# main function
for i in map(lambda x: loadJson(x), findJsonfilename()):
	# if there is no DocByUserToken Collection or new json data has been inserted 
	docByUsertoken(i["user_token"], i)
	stuInfoLog(i["user_token"], i)

