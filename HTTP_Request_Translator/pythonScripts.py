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
	print(skeleton_code)