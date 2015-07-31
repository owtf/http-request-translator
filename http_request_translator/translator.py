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
        description="Request Translator is a standalone tool that can translate "
                    "raw HTTP requests into curl commands or bash/python/php/ruby/PowerShell scripts")
    conflicting_group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        '--output', '-o',
        action='append',
        help="Generates a script for given HTTP request. "
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
        help="Interactive mode: read raw HTTP request from keyboard, hit enter when ready."
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
        headers, details = parse_raw_request(args.Request)
        if args.data:
            details['data'] = args.data
        else:
            details['data'] = None
        if args.proxy:
            details['proxy'] = args.proxy
        if not details['data'] and details['method'].strip().upper() == "POST":
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
                generated_code = generate_script(script, headers, details, arg_option)
                print(generated_code)

    return argdict


def take_headers(script_list):
    """Takes Request headers while interactive mode is active

    :param list script_list: List of names of the languages for which script is to be generated.

    :return: Raw Request Headers passed in the interactive session.
    :rtype: `str`
    """
    headers = []
    print("Enter Ctrl+C to quit. Press Ctrl+D when finished entering.")
    try:
        print(r">>>"),
        while True:
            try:
                uentered = raw_input("")
                headers.append(uentered + "\n")
            except EOFError:
                print("Enter the Body/Parameter(If Any)")
                take_body(headers, script_list)
    except KeyboardInterrupt:
        print("\nThanks for using the interactive mode! Exiting!")
        sys.exit(0)
    return headers


def take_body(headers, script_list):
    """Takes Request body while interactive mode is active.
    Also prints the generated code for languages passed in `script_list` on console.

    :param str headers: Raw request headers feeded in the interactive session.
    :param list script_list: List of names of the languages for which script is to be generated.

    :return: Body for the request passed in interactive session.
    :rtype: `str`
    """
    body = []
    try:
        print(">>>"),
        while True:
            try:
                uentered = raw_input("")
                body.append(uentered + "\n")
            except EOFError:
                try:
                    parsed_tuple = parse_raw_request("".join(headers))
                    parsed_tuple[1]['data'] = "".join(body).strip()
                    if len(script_list) == 0:
                        # Default curl commands if --output option is not passed
                        # Not implemented yet
                        pass
                    else:
                        for script in script_list:
                            generated_code = generate_script(script, parsed_tuple)
                            print(generated_code)
                except ValueError:
                    print("Please Enter a Vaild Request!")
                take_headers(script_list)
    except KeyboardInterrupt:
        print("\nThanks for using the interactive mode! Exiting!")
        sys.exit(0)
    return body


def parse_raw_request(request):
    """Parses Raw HTTP request into separate dictionaries for headers and body and other parameters.

    :param str request: Raw HTTP request.

    :raises ValueError: When request passed in malformed.

    :return: Separate dictionaries for headers and body and other parameters.
    :rtype: dict,dict
    """
    try:
        new_request_method, new_request = request.split('\n', 1)[0], request.split('\n', 1)[1]
    except IndexError:
        raise ValueError("Request Malformed. Please Enter a Valid HTTP request.")
    header_dict = dict(HTTPHeaders.parse(new_request))
    details_dict = {}
    details_dict['method'] = new_request_method.split(' ', 2)[0]
    try:  # try to split the path from request if one is passed.
        proto_ver = new_request_method.split(' ', 2)[2].split('/', 1)
        details_dict['protocol'] = proto_ver[0]
        details_dict['version'] = proto_ver[1]
        details_dict['path'] = new_request_method.split(' ', 2)[1]
    except IndexError:
        details_dict['path'] = ""
        try:
            proto_ver = new_request_method.split(' ', 2)[1].split('/', 1)
        except IndexError:  # Failed to get protocol and version.
            raise ValueError("Request Malformed. Please Enter a Valid HTTP request.")
        details_dict['protocol'],  = proto_ver[0]
        details_dict['version'] = proto_ver[1]
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
        details_dict['pre_scheme'] = scheme + "://"  # Store the scheme defined in GET path for later checks
    else:
        details_dict['pre_scheme'] = ''
    details_dict['Host'] = header_dict['Host']
    return header_dict, details_dict


def main():
    # TODO: Docstring and comments.
    args = take_arguments()

if __name__ == '__main__':
    main()
