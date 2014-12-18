#!/usr/bin/python
import pprint
import re

def generate_script(header_dict, details_dict, searchString=None):
	
	method = details_dict['method'].strip()
        host = details_dict['Host']
        headers = str(header_dict)
        a = re.sub(r"{|}","",headers)
        b = re.sub(r"': '"," : ",a)
        c = re.sub(r"', '","\" --header \"",b)
        d = re.sub(r"\'","\"",c)
        e = re.sub(r"\"Host :","",d)
        formattedHeaders = re.sub(r"\"","",e,1)

	if searchString:
		try:
			if not 'proxy' in details_dict:
 
			        if method == 'POST':
					skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request POST'''+formattedHeaders+''' --include
					'''
			        elif method == 'GET':
					skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request GET'''+formattedHeaders+''' --include > request
replacement = $(tput setaf 1; echo "'''+searchString+'''")
echo ${request//'''+searchString+'''/$replacement}
					'''
			        elif method == 'PUT':
					skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request PUT'''+formattedHeaders+''' --include
					'''
			        elif method == 'DELETE':
					skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request DELETE'''+formattedHeaders+''' --include
					'''
			
			else:

				if method == 'POST':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request POST'''+formattedHeaders+''' --include
					'''
                                elif method == 'GET':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request GET'''+formattedHeaders+''' --include
					'''
                                elif method == 'PUT':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request PUT'''+formattedHeaders+''' --include
					'''
                                elif method == 'DELETE':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request DELETE'''+formattedHeaders+''' --include
					'''
		except IndexError as i :
			print "You haven't given the port Number"
		else :
                       	print (skeleton_code)
	else :
		try :
                        if not 'proxy' in details_dict :

                                if method == 'POST':
                                       	skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request POST'''+formattedHeaders+''' --include
					'''
                                elif method == 'GET':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request GET'''+formattedHeaders+''' --include
					'''
                                elif method == 'PUT':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request PUT'''+formattedHeaders+''' --include
					'''
                                elif method == 'DELETE':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request DELETE'''+formattedHeaders+''' --include
					'''

			else:
				if method == 'POST':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request POST'''+formattedHeaders+''' --include
					'''
                                elif method == 'GET':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request GET'''+formattedHeaders+''' --include
					'''
                                elif method == 'PUT':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request PUT'''+formattedHeaders+''' --include
					'''
                                elif method == 'DELETE':
                                        skeleton_code = '''\
#!/usr/bin/env bash
curl -v --request DELETE'''+formattedHeaders+''' --include
					'''
		except IndexError as i :
			print "You haven't given the port Number"

                else :
			print (skeleton_code)
