#!/usr/bin/python
import pprint

def generate_script(header_dict, details_dict):

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

	try :
		if not 'proxy' in details_dict :
			skeleton_code = '''
			#!/usr/bin/python
			from tornado.httpclient import HTTPRequest, HTTPClient

			def main():
				request_object = HTTPRequest(''' +details_dict['Host']+ \
					''', method=''' +details_dict['method'].strip()+\
					''', headers=''' +str(header_dict)+ ''')
				return HTTPClient().fetch(request_object).headers

			if __name__ == '__main__':
			main()
			'''
		
		else :
			skeleton_code = '''
			#!/usr/bin/python
			from tornado.httpclient import HTTPRequest, HTTPClient

			def main():
				request_object = HTTPRequest(''' +details_dict['Host']+ \
					''', method=''' +details_dict['method'].strip()+\
					''', headers=''' +str(header_dict)+ ''', proxy_host='''\
					+details_dict['proxy'].split(':')[0].strip()+ \
					''', proxy_port=''' +details_dict['proxy'].split(':')[1].strip()+ \
					''')			
				return HTTPClient().fetch(request_object).headers

			if __name__ == '__main__':
			main()
			'''
	
	except IndexError as i :
		print "You haven't given the port Number" 
		
	else :
		print(skeleton_code)