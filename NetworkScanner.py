import subprocess, locale, socket
from socket import gethostbyaddr

encoding = locale.getdefaultlocale()[1]
 
def ping(host):
	response = subprocess.Popen(["ping", "-c", "3", host], stdout=subprocess.PIPE).stdout.read()
	if 'Unreachable' in response.decode(encoding):
		return '%s is Offline' % host
	else:
		return '%s is Alive' % host
 
def scan(get, start, end):
	for n in range(start, end):
		ip = get + '.' + str(n)
		print gethostbyaddr(ip)[0]
		#print(ping(ip))
 
rand = raw_input('Please input your IP: ')
ip_start = int(input('Enter Start Range: '))
ip_end = int(input('Enter Range End: '))
scan(rand, ip_start, ip_end)