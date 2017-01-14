from __future__ import print_function

import sys
import argparse

from .interface import HttpRequestTranslator
from .input_handler import handlers


def init():
    args = take_args()
    hrt = process_args(args)
    codes = hrt.generate_code()
    if args.parse_args().beautify:
        for language in codes:
            print('=' * 5 + ' %s ' % language.upper() + '=' * 5)
            print(codes[language])
    else :
        print(''.join(v for v in codes.values()))


def take_args():
    """Entry point for the translator through CLI. Initializes parser using `argparse` library.

    :return:`argparse.ArgumentParser` instance.
    :rtype:class `argparse.ArgumentParser`
    """
    # TODO: use non-hardcoded list of supported languages.
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
        "--beautify", "-bt",
        action="store_true",
        help="Beautify code printing when multiple languages are selected")
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
    request_group.add_argument(
        "--stdin", "-s",
        action="store_true",
        help="Enable stdin mode for HTTP request")
    return parser


def get_input_type(args):
    """Find input handler with its corresponding parameters based on CLI arguments.

    :param `argparse.Namespace` args: `argparse.Namespace` instance.

    :return: tuple of input type and corresponding options
    :rtype: tuple
    """
    input_type = None
    options = []

    if args.interactive:
        input_type = 'interactive'
    elif args.file:
        input_type = 'file'
        options.append(args.file)
    elif args.request:
        input_type = 'inline'
        options.append(args.request)
    elif args.stdin:
        input_type = 'stdin'

    return (input_type, options)


def get_input(input_type, *options):
    """Takes an input mode type and returns a raw request.

    :raises OSError, IOError: When file fails to open in FileInput mode.

    :return: raw request
    :rtype: str
    """
    if input_type in handlers:
        if options:
            return handlers[input_type](*options)
        else:
            return handlers[input_type]()
    return ''


def process_args(parser):
    """Process the arguments provided to the translator CLI and return a HTTPRequestTranslator object.

    .. note::

        Default language is set to 'bash'.

    :param class `argparse.ArgumentParser`: `argparse.ArgumentParser` instance.

    :raises ValueError: When proxy is invalid.
    :raises NoRequestProvided: When no request is provided.

    :return: HTTPRequestTranslator instance
    :rtype: `HTTPRequestTranslator`
    """
    args = parser.parse_args()
    argdict = vars(args)

    languages = ['bash']  # Default script language is set to bash.
    if argdict.get('language'):
        languages = map(lambda x: x.strip(), argdict['language'][0].split(','))

    input_type, options = get_input_type(args)
    if not input_type:
        parser.print_help()
        sys.exit(-1)

    raw_request = get_input(input_type, *options)

    hrt_obj = HttpRequestTranslator(
        request=raw_request,
        languages=languages,
        proxy=args.proxy,
        search_string=args.search_string,
        data=args.data)

    return hrt_obj
