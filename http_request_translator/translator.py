#!/usr/bin/python
from __future__ import print_function

import sys
import argparse
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from tornado.httputil import HTTPHeaders
from plugin_manager import generate_script


def take_arguments():
    # TODO: Docstring and comments.
    parser = argparse.ArgumentParser(
        description="Request Translator is a standalone tool that can translate "\
                    "raw HTTP requests into curl commands or bash/python/php/ruby/PowerShell scripts")
    conflicting_group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        '--output', '-o',
        action='append',
        help="Generates a script for given HTTP request. "\
             "If you want to generate multiple scripts, separate the script's name with a <,>")
    parser.add_argument(
        '--proxy',
        nargs='?',
        const='127.0.0.1:8009',
        help='Generates command/script with relevant, specified proxy')
    conflicting_group.add_argument(
        '--stringSearch',
        help='Sends the request and searches for the required string in the response (i.e literal match)')
    conflicting_group.add_argument(
        '--regexSearch',
        help='Sends the request and searches for the required regex in the response (i.e regex match)')
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help="Interactive mode: read raw HTTP request from keyboard, hit enter when ready."\
             "Type ':q!' to exit from the interactive mode.")
    parser.add_argument(
        '--data', '-d',
        help='Add the data that you want to send along with the header')
    parser.add_argument(
        '--Request',
        help='Input the HTTP request')
    process_arguments(parser.parse_args())
    return parser.parse_args()


def process_arguments(args):
    # TODO: Docstring and comments.
    argdict = vars(args)
    try:
        script_list = argdict['output'][0].split(',')
    except TypeError:
        script_list = []  # If --output option is not used.
    if args.interactive:
        take_headers(script_list)
    else:
        if not args.Request:
            print("Input a raw HTTP Request and try again.\nElse try using the interactive option")
            sys.exit(-1)
        parsed_tuple = parse_raw_request(args.Request)
        if args.data:
            parsed_tuple[1]['data'] = args.data
        else:
            parsed_tuple[1]['data'] = None
        if args.proxy:
            parsed_tuple[1]['proxy'] = args.proxy
        if not parsed_tuple[1]['data'] and parsed_tuple[1]['method'].strip().upper() == "POST":
            print("Hi there. Send some data to POST, use --data for sending data.")
            sys.exit(-1)
        arg_option = None
        if args.stringSearch:
            arg_option = args.stringSearch
        elif args.regexSearch:
            arg_option = args.regexSearch
        if len(script_list) == 0:
            # Default curl commands if --output option is not passed
            # Not implemented yet
            pass
        else:
            for script in script_list:
                generated_code = generate_script(script, parsed_tuple, arg_option)
                print(generated_code)

    return argdict


def take_headers(script_list):
    # TODO: Docstring and comments.
    headers = []
    print(r">>>"),
    while True:
        uentered = raw_input("")
        if not uentered:
            print("Enter the Body/Parameter ")
            take_body(headers, script_list)
        if uentered == "q!":
            print("Thanks for using the interactive mode!")
            sys.exit(0)
        headers.append(uentered + "\n")
    return headers


def take_body(headers, script_list):
    # TODO: Docstring and comments.
    body = []
    print(">>>"),
    while True:
        uentered = raw_input("")
        if not uentered:
            print("Thank you !")
            parsed_tuple = parse_raw_request("".join(headers))
            parsed_tuple[1]['data'] = "".join(body)
            if len(script_list) == 0:
                # Default curl commands if --output option is not passed
                # Not implemented yet
                pass
            else:
                for script in script_list:
                    generated_code = generate_script(script, parsed_tuple)
                    print(generated_code)
            take_headers(script_list)
        if uentered == "q!":
            print("Thanks for using the interactive mode!")
            sys.exit(0)
        body.append(uentered + "\n")
    return body


def parse_raw_request(request):
    # TODO: Docstring and comments.
    new_request_method, new_request = request.split('\n', 1)[0], request.split('\n', 1)[1]
    header_dict = dict(HTTPHeaders.parse(new_request))
    details_dict = {}
    details_dict['method'] = new_request_method.split(' ', 2)[0]
    try:
        details_dict['protocol'], details_dict['version'] = new_request_method.split(
            ' ', 2)[2].split('/', 1)[0], new_request_method.split(' ', 2)[2].split('/', 1)[1]
        details_dict['path'] = new_request_method.split(' ', 2)[1]
    except IndexError:
        details_dict['path'] = ""
        details_dict['protocol'], details_dict['version'] = new_request_method.split(
            ' ', 2)[1].split('/', 1)[0], new_request_method.split(' ', 2)[1].split('/', 1)[1]
    # Parse the GET Path to update it to only contain the relative path and not whole url
    # scheme://netloc/path;parameters?query#fragment
    # Eg: Path=https://google.com/robots.txt to /robots.txt
    scheme, netloc, path, params, query, frag = urlparse(details_dict['path'])
    if params:
        path = path+";"+params
    if query:
        path = path+"?"+query
    if frag:
        path = path+"#"+frag
    details_dict['path'] = path
    # If scheme is specified in GET Path and Header 'Host' Field doesn't already starts with it
    if scheme and not header_dict['Host'].startswith(scheme):
        # Check if Host Field already has port specified
        if ":" not in header_dict['Host'] and not netloc.startswith('['):
            if scheme == "https":
                header_dict['Host'] += ":443"
        else:
            #  If no port is specified for address like [::1]
            if header_dict['Host'].endswith(']'):
                if scheme == "https":
                    header_dict['Host'] += ":443"
    details_dict['Host'] = header_dict['Host']
    return header_dict, details_dict


def main():
    # TODO: Docstring and comments.
    args = take_arguments()

if __name__ == '__main__':
    main()
