#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient
import pprint
def generate_skeleton(header_dict, details_dict):

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