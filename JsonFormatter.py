from datetime import datetime, timedelta

def strToInt(js_dict):
	## Some strings need to be changed as an integer type.
	for key, val in js_dict.items():
		if type(val) != list:
			if key == "measurement_datetime":
				js_dict[key] = datetime.strptime(val, "%Y-%m-%d %H:%M:%S") + timedelta(hours=7)
			if val.isnumeric():
				js_dict[key] = int(val)
		elif type(val) == list:
			for json_dict in val:
				strToInt(json_dict)
	return js_dict

