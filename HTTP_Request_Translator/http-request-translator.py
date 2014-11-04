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

	parser.add_argument('HTTPRequest',
		help='Input the HTTP request')


	process_arguments(parser.parse_args())
	return parser.parse_args()


def process_arguments(args):
	default = True
	script_list = []
	argdict = vars(args)
	for i in argdict :
		if argdict[i] == True:
			script_list.append(i)

	if 'interactive' in script_list :
		script_list.remove('interactive')
		interactive_mode(script_list)

	else:
		if args.HTTPRequest == False :
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
			parsed_dict = parse_raw_request(args.HTTPRequest)
			generate_scripts(script_list, parsed_dict)

	return argdict


def generate_scripts(script_list, parsed_dictionary):

	default = True
	if 'python' in script_list:
		default = False
		pass

	if 'ruby' in script_list :
		default = False
		pass

	if 'php' in script_list :
		default = False
		pass

	if 'bash' in script_list :
		default = False
		pass

	if default :
		#generates the default Curl command
		pass


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
    if chunk.strip() == "exit":
        sys.exit(0)
    else:
        parsed_dictionary = parse_raw_request(chunk)
        generate_scripts(script_list, parsed_dictionary)

					


def parse_raw_request(request):

	new_request = request.encode('string-escape').split(r'\n', 1)[1]
	h = HTTPHeaders.parse(str(new_request))
	return dict(h)

def main():
	args = take_arguments()

if __name__ == '__main__':
	main()