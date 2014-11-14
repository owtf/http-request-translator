#!/usr/bin/python
import argparse, re, sys
from tornado.httputil import HTTPHeaders


def take_arguments():
	parser = argparse.ArgumentParser(description=
		"<insert it later>")
	conflicting_group = parser.add_mutually_exclusive_group()

	parser.add_argument('--ruby','-r',
		help='Generate a ruby script for given HTTP request',
		action='store_true')

	parser.add_argument('--python', '-py',
		help='Generate a python script for given HTTP request',
		action='store_true')

	parser.add_argument('--bash', '-sh',
		help='Generate a bash script for given HTTP request',
		action='store_true')

	parser.add_argument('--php',
		help='Generate a PHP script for given HTTP request',
		action='store_true')

	parser.add_argument('--curl', '-c',
		help='Generate a Curl command for given HTTP request',
		action='store_true')

	parser.add_argument('--proxy',
		nargs='?',
		const='127.0.0.1:8009',
		help='Generates command/script with relevant,\
		specified proxy')

	conflicting_group.add_argument('--string-search',
		help='Sends the request and searches for the\
		required string in the response(i.e literal match)',
		action='store_true')

	conflicting_group.add_argument('--regex-search',
		help='Sends the request and searches for the\
		required regex in the response(i.e regex match)',
		action='store_true')

	parser.add_argument('--interactive', '-i',
		help='Interactive mode: read raw HTTP request from keyboard,\
	 	hit enter when ready.Type exit to exit the interactive mode.',
		action='store_true')

	parser.add_argument('--Request',
		help='Input the HTTP request',
		)


	process_arguments(parser.parse_args())
	return parser.parse_args()


def process_arguments(args):
	default = True
	script_list = []
	argdict = vars(args)
	for i in argdict :
		if argdict[i] == True:
			script_list.append(i)

	if args.interactive :
		script_list.remove('interactive')
		interactive_mode(script_list)

	else:
		if not args.Request:
			print "Input a raw HTTP Request and try again\
			" +"\n"+"Else try using the interactive option"
			sys.exit(0)

		if 'string-search' in script_list :
			script_list.remove('string-search')
			pass

		elif 'regex-search' in script_list :
			script_list.remove('regex-search')			
			pass

		else:
			parsed_dict = parse_raw_request(args.Request)
			generate_scripts(script_list, parsed_dict)

	return argdict


def generate_scripts(script_list, parsed_tuple):

	default = True
	if 'python' in script_list:
		default = False
		import pythonScripts
		port_protocol = {'https' : 443, 'ssh' : 22, 'ftp' : 21,'ftp' : 20, 'irc' : 113}
		url = str(parsed_tuple[0]['Host'])
		try :
			protocol = url.split(':', 2)[2]
			if protocol in port_protocol.keys():
				prefix = str(port_protocol[key]) + "://"
			else :
				prefix = "http://"
				
		except IndexError:
			prefix = "http://"
		url = prefix + str(parsed_tuple[0]['Host'])
		parsed_tuple[1]['Host'] = url
		pythonScripts.generate_skeleton(parsed_tuple[0], parsed_tuple[1])

	if 'ruby' in script_list :
		default = False
		import rubyScripts
		rubyScripts.skeleton(parsed_dictionary)

	if 'php' in script_list :
		default = False
		import phpScripts
		phpScripts.skeleton(parsed_dictionary)

	if 'bash' in script_list :
		default = False
		import bashScripts
		bashScripts.skeleton(parsed_dictionary)

	if default :
		#generates the default Curl command
		import default
		default.skeleton(parsed_dictionary)


def interactive_mode(script_list):

	buf = []
	print "Enter the HTTP request. Once entered,\
	Press enter again! And type ':q!' to exit "

	while True:
	    http_request = raw_input(">>" + '\n')
	    if not http_request:
	        take_interactive_params("".join(buf), script_list)
	        buf = []
	    buf.append(http_request + "\n")


def take_interactive_params(chunk, script_list):
    if chunk.strip() == ":q!":
        sys.exit(0)
    else:
        parsed_dictionary = parse_raw_request(chunk)
        generate_scripts(script_list, parsed_dictionary)

def parse_raw_request(request):

	new_request_method, new_request = \
	request.split('\n', 1)[0], request.split('\n', 1)[1]
	header_dict = dict(HTTPHeaders.parse(new_request))
	details_dict = {}
	details_dict['method'], details_dict['protocol'], details_dict['version'],\
	details_dict['Host'] = new_request_method.split('/', 2)[0],new_request_method.split('/', 2)[1],\
	new_request_method.split('/', 2)[2], header_dict['Host']
	return header_dict, details_dict


def main():
	args = take_arguments()

if __name__ == '__main__':
	main()