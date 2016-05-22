import argparse
import os

from .exceptions import NoRequestProvided
from .interface import HttpRequestTranslator


def init():
    args = take_args()
    hrt_obj = process_args(args)
    hrt_obj.generate_code()


def take_args():
    """Entry point for the translator through CLI. Parses arguments using `argparse` library.

    :return:`argparse` class object containing arguments passed to the translator.
    :rtype:class `argparse.Namespace`
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

    return parser.parse_args()


def get_interactive_request():
    raw_request = []
    print "Enter raw request - "
    while True:
        try:
            raw_request.append(raw_input().strip())
        except EOFError:
            break
    return '\n'.join(raw_request).strip()


def get_request_from_file(filepath):
    if not os.path.exists(filepath):
        raise IOError

    raw_request = open(filepath).read()
    return raw_request


def process_args(args):
    """Process the arguments provided to the translator CLI and return a HTTPRequestTranslator object.

    :param class `argparse.Namespace`: `argparse` class object containing arguments passed to the translator.

    :raises ValueError: When proxy is invalid.
    :raises NoRequestProvided: When no request is provided.

    :return: HTTPRequestTranslator object
    :rtype: `HTTPRequestTranslator`
    """
    argdict = vars(args)

    script_list = ['bash'] # default script language is set to bash
    if argdict.get('language'):
        languages = map(lambda x: x.strip(), argdict['language'][0].split(','))

    # fetch raw request from either of the three sources.
    raw_request = ""
    if args.interactive:
        # get_interactive_request will handle input and formation of raw request.
        raw_request = get_interactive_request()
    elif args.request:
        raw_request = args.request
    elif args.file:
        raw_request = get_request_from_file(args.file)
    else:
        raise NoRequestProvided

    hrt_obj = HttpRequestTranslator(request=raw_request, languages=languages, proxy=args.proxy,
        search_string=args.search_string, data=args.data)
    return hrt_obj
