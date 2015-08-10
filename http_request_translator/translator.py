#!/usr/bin/python
from __future__ import print_function

import sys
import argparse
try:
    input = raw_input  # Python 2.x
except NameError:
    pass  # Python 3.x
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from .plugin_manager import generate_script
from .url import get_url, check_valid_url


def take_arguments():
    """Entry point for the translator. Parses arguments using `argparse` library.

    :return:`argparse` class object containing arguments passed to the translator.
    :rtype:class `argparse.Namespace`
    """
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
        '--proxy', '-p',
        nargs='?',
        const='127.0.0.1:8009',
        help='Generates command/script with relevant, specified proxy')
    conflicting_group.add_argument(
        '--string_search', '-s',
        help='Sends the request and searches for the required string in the response (i.e literal match)')
    conflicting_group.add_argument(
        '--regex_search', '-re',
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
        '--request', '-r',
        help='Input the HTTP request')
    process_arguments(parser.parse_args())
    return parser.parse_args()


def process_arguments(args):
    """Process the arguments provided to the translator and places values in separate headers and details dictionaries.

    :param class `argparse.Namespace`: `argparse` class object containing arguments passed to the translator.

    :raises ValueError: When proxy provided is invalid.

    :return: A dictionaries of arguments passed.
    :rtype: `dict`
    """
    argdict = vars(args)
    try:
        script_list = argdict['output'][0].split(',')
    except TypeError:
        script_list = []  # If --output option is not used.
    if args.interactive:
        try:
            take_headers(script_list)
        except KeyboardInterrupt:
            print("\nThanks for using the interactive mode! Exiting!")
            sys.exit(0)
    else:
        if not args.request:
            print("Input a raw HTTP Request and try again.\nElse try using the interactive option")
            sys.exit(-1)
        headers, details = parse_raw_request(args.request)
        if args.data:
            details['data'] = args.data
        else:
            details['data'] = None
        if args.proxy:
            # If proxy already doesn't starts with http and is like 127.0.0.1:8010
            if not args.proxy.startswith(('http', 'https')):
                proxy = get_url(args.proxy)  # Fix proxy to add appropriate scheme
            else:
                proxy = args.proxy.strip()
            if not check_valid_url(proxy):
                raise ValueError("Proxy provided is invalid.")
            try:
                details['proxy_host'], details['proxy_port'] = proxy.rsplit(":", 1)
            except IndexError:
                raise ValueError("Proxy provided is invalid.")
        if not details['data'] and details['method'].strip().upper() == "POST":
            print("Hi there. Send some data to POST, use --data for sending data.")
            sys.exit(-1)
        arg_option = None
        if args.string_search:
            arg_option = args.string_search
        elif args.regex_search:
            arg_option = args.regex_search
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
    print("Enter request headers (Ctrl+D to finish/Ctrl+C to quit).")
    while True:
        try:
            uentered = input(">>> ")
            headers.append(uentered + "\n")
        except EOFError:
            take_body(headers, script_list)
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
    print("\nEnter request body/parameters (Ctrl+D to finish/Ctrl+C to quit).")
    while True:
        try:
            uentered = input(">>> ")
            body.append(uentered + "\n")
        except EOFError:
            try:
                headers, details = parse_raw_request("".join(headers))
                details['data'] = "".join(body).strip()
                if not script_list:
                    # TODO: Default curl commands if --output option is not passed
                    # Not implemented yet
                    pass
                else:
                    for script in script_list:
                        print(generate_script(script, headers, details))
            except ValueError:
                print("Please Enter a Vaild Request!")
            take_headers(script_list)
    return body


def parse_raw_request(request):
    """Parses Raw HTTP request into separate dictionaries for headers and body and other parameters.

    :param str request: Raw HTTP request.

    :raises ValueError: When request passed in malformed.

    :return: Separate dictionaries for headers and body and other parameters.
    :rtype: dict,dict
    """
    try:
        new_request_method, headers = request.split('\n', 1)
    except IndexError:
        raise ValueError("Request Malformed. Please Enter a Valid HTTP request.")

    header_list = []
    for line in headers.splitlines():
        header_list.append(line)
        try:
            header, value = line.split(":", 1)
        except IndexError:
            raise ValueError("Headers Malformed. Please Enter a Valid HTTP request.")
        if header.lower() == "host":
            host = value.strip()  # Keep hostname for further checks

    details_dict = {}
    details_dict['method'] = new_request_method.split(' ', 1)[0].strip()
    details_dict['Host'] = host
    # Not using whatever stored in parsed_request for the reason to keep the request as original as possible
    try:  # try to split the path from request if one is passed.
        proto_ver = new_request_method.split(' ', 2)[2].split('/', 1)
        details_dict['protocol'] = proto_ver[0].strip()
        details_dict['version'] = proto_ver[1].strip()
        details_dict['path'] = new_request_method.split(' ', 2)[1].strip()
    except IndexError:
        details_dict['path'] = ""
        try:
            proto_ver = new_request_method.split(' ', 2)[1].split('/', 1)
        except IndexError:  # Failed to get protocol and version.
            raise ValueError("Request Malformed. Please Enter a Valid HTTP request.")
        details_dict['protocol'] = proto_ver[0].strip()
        details_dict['version'] = proto_ver[1].strip()
    # Parse the GET Path to update it to only contain the relative path and not whole url
    # scheme://netloc/path;parameters?query#fragment
    # Eg: Path=https://google.com/robots.txt to /robots.txt
    scheme, netloc, path, params, query, frag = urlparse(details_dict['path'])
    if params:
        path = path + ";" + params
    if query:
        path = path + "?" + query
    if frag:
        path = path + "#" + frag
    details_dict['path'] = path
    # If scheme is specified in GET Path and Header 'Host' Field doesn't already starts with it
    if scheme and not host.startswith(scheme):
        details_dict['pre_scheme'] = scheme + "://"  # Store the scheme defined in GET path for later checks
    else:
        details_dict['pre_scheme'] = ''
    return header_list, details_dict


def main():
    # TODO: Docstring and comments.
    take_arguments()

if __name__ == '__main__':
    main()
