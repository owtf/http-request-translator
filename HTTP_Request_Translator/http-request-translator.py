#!/usr/bin/python
impo#!/usr/bin/python
import argparse, re

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
		default='127.0.0.1:8009',
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

	parser.add_argument('HTTP Request',
		help='Input the HTTP request')


	process_arguments(parser.parse_args())
	return parser.parse_args()



def process_arguments(args):

	proxy = None
	if args.proxy:
		proxy=args.proxy

	if args.interactive :
		interactive_mode(args, proxy)
	
	elif args.regex-search or args.string-search :
		pass

	else :
		if args.python :
			pass

		elif args.ruby :
			pass

		elif args.php :
			pass

		elif args.bash :
			pass

		else :
			pass


def interactive_mode(args, proxy):

	while (True):
		http_request = input("Enter the HTTP Request")
		if http_request == "exit":
			break
		else:
			parsed_dictionary = parse_raw_request(http_request)
			if parsed_dictionary['request_type'] or parsed_dictionary['host'] is None:
				print "Invalid HTTP Request"
				break
			else:
				if args.python :
					pass

				elif args.ruby :
					pass

				elif args.php :
					pass

				elif args.bash :
					pass

				else :
					pass
					#The functionality will be added after adding the required methods in default.py
					pass


def parse_raw_request(request):

	request_type = "GET"
	type_match = re.search(r'^POST', request)
	if type_match:
		request_type = "POST"
	type_match = re.search(r'^PUT', request)
	if type_match:
		request_type = "PUT"
	type_match = re.search(r'^HEAD', request)
	if type_match:
		request_type = "HEAD"
	type_match = re.search(r'^DELETE', request)
	if type_match:
		request_type = 'Delete'

	host_match = re.search(r'Host: [\w \d .-]+', request)
	if host_match:
		host = host_match.group().split(':', 1)[1]

	user_agent_match = re.search(r'User-Agent: [\w \d .-/();]+', request)
	if user_agent_match:
		user_agent = user_agent_match.group().split(':', 1)[1]

	content_length_match = re.search(r'Content-Length: [\d]+ ', request)
	if content_length_match:
		content_length = content_length_match.group().split(':', 1)[1]

	return {'request_type': request_type, 
			'host': host,
			'user_agent': user_agent,
			'content_length': content_length}


def main():
	args = take_arguments()

if __name__ == '__main__':
	main()