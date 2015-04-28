import os
import sys
import json
import subprocess

dirname = "BonafideMeasurement_result"
# directory name for storing result files

def makeDir(dirname):
	# directory will be automatically made if it not exists
	if not os.path.exists(dirname):
		os.makedirs(dirname)

def executeCurl():
	# if user token is entered, then curl command will be executed using subprocess
	curlcmd = ['curl', 'https://bonafide.pw/rest/measurement-results/list/' + usertoken]
	subp = subprocess.Popen(curlcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	curlstdout, curlstderr = subp.communicate()
	jsonCurled = json.loads(curlstdout) 
	# result will be loaded as json
	print validUsertoken(jsonCurled)

def validUsertoken(jCurled):
	# To check whether the entered usertoken is valid
	validationResponse = ""
	if len(jCurled["measurement_results"]) == 0:
		# if user token is not valid 
		validationResponse = "Check your usertoken again"
	else:
		filename = usertoken + "_jsonfile.json"
		with open(dirname+"/"+filename, 'wb') as outfile:
			# os.path.join also ensures complete path and filename. I use a easiest way..
			json.dump(jCurled, outfile, indent=4, sort_keys=True)
			# Valid user token will make json file in the directory that has been made
			validationResponse = "measurement result is saved as " + filename
	return validationResponse


# main process
if len(sys.argv) == 1:
  print "Input the usertoken"
else:
	usertoken = sys.argv[1]
	makeDir(dirname)
	executeCurl()



