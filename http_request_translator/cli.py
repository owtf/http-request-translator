from __future__ import print_function

import sys
import json
import argparse

from .interface import HttpRequestTranslator


try:
    input = raw_input  # Python2/3 version
except NameError:
    pass


def init():
    parser = take_args()
    hrt_obj = process_args(parser)
    print(json.dumps(hrt_obj.generate_code(), indent=4))


def take_args():
    """Entry point for the translator through CLI. Initializes parser using `argparse` library.

    :return:`argparse.ArgumentParser` instance.
    :rtype:class `argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(
        description="Request Translator is a standalone tool that can translate "
                    "raw HTTP requests into bash/python/php/ruby scripts")
    request_group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "--language", "-l",
        action="append",
        help="Generates a script in language 'language' for given HTTP request. "
            "If you want to generate multiple scripts, separate the script's name with a <,>. "
            "Available languages: bash, php, python, ruby")
    parser.add_argument(
        "--proxy", "-p",
        nargs="?",
        const="127.0.0.1:8009",
        help="Generates command/script with relevant, specified proxy")
    parser.add_argument(
        "--search_string", "-ss",
        help="Sends the request and searches for the required string in the response (regex can be provided)")
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive mode: read raw HTTP request from keyboard, hit enter when ready. Type 'Ctrl+D' or 'Ctrl+C'"
            "to exit from the interactive mode.")
    parser.add_argument(
        "--data", "-d",
        help="Add the data that you want to send along with the header")
    request_group.add_argument(
        "--request", "-r",
        help="Input the HTTP request")
    request_group.add_argument(
        "--file", "-f",
        help="Input file for HTTP request")
    return parser


def get_interactive_request():
    raw_request = []
    print("Enter raw request - ")
    while True:
        try:
            raw_request.append(input().strip())
        except (EOFError, KeyboardInterrupt):
            break
    return '\n'.join(raw_request).strip()


def process_args(parser):
    """Process the arguments provided to the translator CLI and return a HTTPRequestTranslator object.


def process_args(args):
    """Process the arguments provided to the translator CLI and return a HTTPRequestTranslator object.

    :param class `argparse.ArgumentParser`: `argparse.ArgumentParser` instance.

    :raises ValueError: When proxy is invalid.
    :raises NoRequestProvided: When no request is provided.

    :return: HTTPRequestTranslator instance
    :rtype: `HTTPRequestTranslator`
    """
    args = parser.parse_args()
    argdict = vars(args)

    languages = ['bash'] # default script language is set to bash
    if argdict.get('language'):
        languages = map(lambda x: x.strip(), argdict['language'][0].split(','))

    # fetch raw request from either of the three sources.
    raw_request = ""
    if args.interactive:
        raw_request = get_interactive_request()
    elif args.request:
        raw_request = args.request
    elif args.file:
        try:
            raw_request = open(args.file).read()
        except (OSError, IOError) as e:
            sys.stderr.write("error: Failed to open '%s'\n\n" % args.file)
            raise e
    else:
        sys.stderr.write("error: Input a valid HTTP request or use interactive mode instead.\n\n")
        parser.print_help()
        sys.exit(-1)

    hrt_obj = HttpRequestTranslator(
        request=raw_request,
        languages=languages,
        proxy=args.proxy,
        search_string=args.search_string,
        data=args.data)
    return hrt_obj
