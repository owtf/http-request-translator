#!/usr/bin/python
import pprint
import re

def generate_script(header_dict, details_dict):
	
	method = details_dict['method'].strip()
	host = details_dict['Host']
	headers = str(header_dict)
	a = re.sub(r"{|}","",headers)
	b = re.sub(r"': '"," : ",a)
	c = re.sub(r"', '","\" --header \"",b)
	formattedHeaders = re.sub(r"\'","\"",c)

        if method == 'POST':
		skeleton_code = '''
		#!/usr/bin/env bash
		curl -v --request POST '''+host+''' --header '''+headers+''' --include
                '''
        elif method == 'GET':
		skeleton_code = '''
		#!/usr/bin/env bash
		curl -v --request GET '''+host+''' --header '''+formattedHeaders+''' --include
		'''
        elif method == 'PUT':
		skeleton_code = '''
		#!/usr/bin/env bash
		curl -v --request PUT '''+host+''' --header '''+headers+''' --include
                '''
        elif method == 'DELETE':
		skeleton_code = '''
		#!/usr/bin/env bash
		curl -v --request DELETE '''+host+''' --header '''+headers+''' --include
                '''
	print (skeleton_code)
