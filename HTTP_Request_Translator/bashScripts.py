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
 
			        skeleton_code = '''\
#!/usr/bin/env bash
curl -s --request '''+method+formattedHeaders+''' --include | egrep --color '''+"'"+searchString+'''|$'
				'''
			
			else:

				skeleton_code = '''\
#!/usr/bin/env bash
curl -x '''+details_dict['proxy']+''' -s --request '''+method+formattedHeaders+''' --include | egrep --color '''+"'"+searchString+'''|$'
				'''
		except IndexError as i :
			print "You haven't given the port Number"
		else :
                       	print (skeleton_code)
	else :
		try :
                        if not 'proxy' in details_dict :

				skeleton_code = '''\
#!/usr/bin/env bash
curl -s --request '''+method+formattedHeaders+''' --include
				'''
			else:
				skeleton_code = '''\
#!/usr/bin/env bash
curl -x '''+details_dict['proxy']+''' -s --request '''+method+formattedHeaders+''' --include
				'''
		except IndexError as i :
			print "You haven't given the port Number"

                else :
			print (skeleton_code)
