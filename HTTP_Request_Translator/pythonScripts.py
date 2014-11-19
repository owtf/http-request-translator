#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient
from termcolor import colored

import pprint, re

def generate_script(header_dict, details_dict, searchString=None):

	port_protocol = {'https' : 443, 'ssh' : 22, 'ftp' : 21,'ftp' : 20, 'irc' : 113}
	url = str(header_dict['Host'])
	try :
		protocol = url.split(':', 2)[2]
		if protocol in port_protocol.keys():
			prefix = str(port_protocol[key]) + "://"
		else :
			prefix = "http://"
			
	except IndexError:
		prefix = "http://"
	url = prefix + str(header_dict['Host'])
	details_dict['Host'] = url

	if searchString :
		try :
			if not 'proxy' in details_dict :
				skeleton_code = '''\
#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient
from termcolor import colored
import re

def main():
	headers, url, method = ''' +str(header_dict)+ ''', "''' +url+ '''" , "''' +details_dict['method'].strip()+ '''"
	request_object = HTTPRequest(url, method=method,headers=headers)		
	response_header = HTTPClient().fetch(request_object).headers
	response_header = re.sub("''' +str(searchString)+ '''", str(colored("''' +str(searchString)+ '''", 'green')), str(response_header))
	print response_header
			
if __name__ == '__main__':
	main()

				'''
			else :
				skeleton_code = '''\
#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient
from termcolor import colored
import re


def main():

	headers, url, method = ''' +str(header_dict)+ ''', "''' +url+\
	'''" , "''' +details_dict['method'].strip()+ '''"
	proxy_host, proxy_port = "''' +details_dict['proxy'].split(':')[0].strip()+\
	'''", "''' +details_dict['proxy'].split(':')[1].strip()+ '''"
	request_object = HTTPRequest(url, method=method, headers=headers, proxy_host=proxy_host, proxy_port=proxy_port)
	response_header = HTTPClient().fetch(request_object).headers
	response_header = re.sub("''' +str(searchString)+ '''", str(colored("''' +str(searchString)+ '''", 'green')), str(response_header))
	return request_object


if __name__ == '__main__':
	main()
				'''

		except IndexError as i :
			print "You haven't given the port Number" 
		else :
			print skeleton_code

	else :
		try :
			if not 'proxy' in details_dict :
				skeleton_code = '''\
#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient

def main():
	headers, url, method = ''' +str(header_dict)+ ''', "''' +url+ '''" , "''' +details_dict['method'].strip()+ '''"
	request_object = HTTPRequest(url, method=method,headers=headers)		
	response_header = HTTPClient().fetch(request_object).headers
	print response_header
			
if __name__ == '__main__':
	main()
				'''
			
			else :
				skeleton_code = '''\
#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient


def main():

	headers, url, method = ''' +str(header_dict)+ ''', "''' +url+\
	'''" , "''' +details_dict['method'].strip()+ '''"
	proxy_host, proxy_port = "''' +details_dict['proxy'].split(':')[0].strip()+\
	'''", "''' +details_dict['proxy'].split(':')[1].strip()+ '''"
	request_object = HTTPRequest(url, method=method, headers=headers, proxy_host=proxy_host, proxy_port=proxy_port")			
	return HTTPClient().fetch(request_object).headers


if __name__ == '__main__':
	main()
				'''
		
		except IndexError as i :
			print "You haven't given the port Number" 
			
		else :
			print(skeleton_code)
