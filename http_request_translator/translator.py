#!/usr/bin/python

from tornado.httputil import HTTPHeaders

from translatorPlugin import pluginManager
import argparse
import re
import sys


def take_arguments():

    parser = argparse.ArgumentParser(description='Request Translator is a standalone tool that can translate \
         raw HTTP requests into curl commands or \
         bash/python/php/ruby/PowerShell scripts')

    conflicting_group = parser.add_mutually_exclusive_group()

    parser.add_argument('--output', '-o',
                        help='Generates a script for given HTTP request. \
        If you want to generate multiple scripts, separate the script\'s name with a <,> ',
                        action='append')

    parser.add_argument('--proxy',
                        nargs='?',
                        const='127.0.0.1:8009',
                        help='Generates command/script with relevant,\
        specified proxy')

    conflicting_group.add_argument('--stringSearch',
                                   help='Sends the request and searches for the\
        required string in the response(i.e literal match)',
                                   )

    conflicting_group.add_argument('--regexSearch',
                                   help='Sends the request and searches for the\
        required regex in the response(i.e regex match)',
                                   )

    parser.add_argument('--interactive', '-i',
                        help='Interactive mode: read raw HTTP request from keyboard,\
        hit enter when ready.Type ":q!" to exit from the interactive mode.',
                        action='store_true')

    parser.add_argument('--data', '-d',
                        help='Add the data that you want to send along with the header'
                        )

    parser.add_argument('--Request',
                        help='Input the HTTP request',
                        )

    process_arguments(parser.parse_args())
    return parser.parse_args()


def process_arguments(args):

    argdict = vars(args)

    try:
        script_list = argdict['output'][0].split(',')

    except TypeError:
        # If --output option is not used
        script_list = []

    if args.interactive:
        take_headers(script_list)

    else:
        if not args.Request:
            print "Input a raw HTTP Request and try again\
            " + "\n" + "Else try using the interactive option"
            sys.exit(0)

        parsed_tuple = parse_raw_request(args.Request)

        if args.data:
            parsed_tuple[1]['data'] = args.data

        else:
            parsed_tuple[1]['data'] = None

        if args.proxy:
            parsed_tuple[1]['proxy'] = args.proxy

        if not parsed_tuple[1]['data'] and parsed_tuple[1]['method'].strip().upper() == "POST":
            print "Hi there. Send some data to POST, use --data for sending data."
            sys.exit(0)

        if args.stringSearch:
            pluginManager(script_list, parsed_tuple, args.stringSearch)

        elif args.regexSearch:
            pluginManager(script_list, parsed_tuple, args.regexSearch)

        else:
            pluginManager(script_list, parsed_tuple)

    return argdict


def take_headers(script_list):

    headers = []
    print(r">>>"),
    while (True):
        uentered = raw_input("")

        if not uentered:
            print "Enter the Body/Parameter "
            take_body(headers, script_list)

        if uentered == "q!":
            print "Thanks for using the interactive mode!"
            sys.exit(0)

        headers.append(uentered + "\n")
    return headers


def take_body(headers, script_list):

    body = []
    print(">>>"),
    while True:
        uentered = raw_input("")

        if not uentered:
            print "Thank you !"
            parsed_tuple = parse_raw_request("".join(headers))
            parsed_tuple[1]['data'] = "".join(body)
            pluginManager(script_list, parsed_tuple)
            take_headers(script_list)

        if uentered == "q!":
            print "Thanks for using the interactive mode!"
            sys.exit(0)

        body.append(uentered + "\n")

    return body


def parse_raw_request(request):

    new_request_method, new_request = \
        request.split('\n', 1)[0], request.split('\n', 1)[1]
    header_dict = dict(HTTPHeaders.parse(new_request))
    details_dict = {}
    details_dict['method'], details_dict['protocol'], details_dict['version'],\
        details_dict['Host'] = new_request_method.split('/', 2)[0],\
        new_request_method.split('/', 2)[1],\
        new_request_method.split('/', 2)[2], header_dict['Host']
    return header_dict, details_dict


def main():
    args = take_arguments()

if __name__ == '__main__':
    main()
