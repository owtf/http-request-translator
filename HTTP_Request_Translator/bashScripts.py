#!/usr/bin/python
import pprint

def generate_skeleton(header_dict, details_dict):
	
	method = details_dict['method'].strip()
	host = details_dict['Host']
	headers = str(header_dict)

        if method == 'POST'{
		skeleton_code = '''
		#!/usr/bin/env bash
		curl --request POST '''host''' --header '''headers''' --include
                '''
        }
        elif method == 'GET'{
		skeleton_code = '''
		#!/usr/bin/env bash
		curl --request GET '''host''' --header '''headers''' --include
		'''
        }
        elif method == 'PUT'{
		skeleton_code = '''
		#!/usr/bin/env bash
		curl --request PUT '''host''' --header '''headers''' --include
                '''
        }
        elif method == 'DELETE'{
		skeleton_code = '''
		#!/usr/bin/env bash
		curl --request DELETE '''host''' --header '''headers''' --include
                '''
        }

	print (skeleton_code)
