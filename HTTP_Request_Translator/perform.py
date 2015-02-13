#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient

def main():
	headers, url, method = {'Content-Type': 'text/html', 'Content-Length': '0', 'Accept': '*/*'}, "http://demo.testfire.net" , "GET"
	body = None
	request_object = HTTPRequest(url, method=method,headers=headers, body=body, allow_nonstandard_methods=True)		
	response_header = HTTPClient().fetch(request_object).headers
	print response_header
			
if __name__ == '__main__':
	main()
				
