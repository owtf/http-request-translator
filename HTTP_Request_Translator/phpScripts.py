#!/usr/bin/python
import pprint
import re

def generate_script(header_dict, details_dict, searchString=None):
	
	method = details_dict['method'].strip()
        host = details_dict['Host']
        headers = str(header_dict)

	if searchString:
		try:
			if not 'proxy' in details_dict:
 
			        skeleton_code = '''\
<?php
$curl = curl_init();
curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => '''+"'"+host+"',"+'''
));
$response = curl_exec($curl);
curl_close($curl);
return $response
?>'''
			
			else:

				skeleton_code = '''\
<?php
$curl = curl_init();
curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => '''+"'"+host+"',"+'''
));
$response = curl_exec($curl);
curl_close($curl);
return $response
?>'''

		except IndexError as i :
			print "You haven't given the port Number"
		else :
                       	print (skeleton_code)
	else :
		try :
                        if not 'proxy' in details_dict :

				skeleton_code = '''\
<?php
$curl = curl_init();
curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => '''+"'"+host+"',"+'''
));
$response = curl_exec($curl);
curl_close($curl);
return $response
?>'''

			else:
				skeleton_code = '''\
<?php
$curl = curl_init();
curl_setopt_array($curl, array(
        CURLOPT_RETURNTRANSFER => 1,
        CURLOPT_URL => '''+"'"+host+"',"+'''
));
$response = curl_exec($curl);
curl_close($curl);
return $response
?>'''

		except IndexError as i :
			print "You haven't given the port Number"

                else :
			print (skeleton_code)
