from __future__ import print_function

import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from url import get_url, check_valid_url
from templates import bash_template


def generate_script(header_dict, details_dict, searchString=None):
    """Generate the bash script for the passed request.

    :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.
    :param dict details_dict: Request specific details like body and method for the request.
    :param str searchString: String to search for in the response to the request. By default remains None.

    :raises ValueError: When url is Invalid

    :return: A combined string of generated code
    :rtype:`str`
    """
    method = details_dict['method']
    url = get_url(header_dict['Host'], details_dict['pre_scheme'])
    url += details_dict['path']

    encoding_list = ['HEAD', 'OPTIONS', 'GET']

    if details_dict['data'] and (details_dict['method'] in encoding_list):
        encoded_data = quote(details_dict['data'], '')
        url = url + encoded_data

    if not check_valid_url(url):
        raise ValueError("Invalid URL")

    skeleton_code = bash_template.begin_code
    skeleton_code += generate_proxy_code(details_dict)
    headers = generate_request_headers(header_dict)
    skeleton_code += bash_template.code_simple.format(method=method, url=url, headers=headers)
    if method == "GET":
        pass
    elif method == "POST":
        skeleton_code += generate_body_code(details_dict['data'])
    else:
        print("Only GET and POST requests are supported yet!")
        return ""

    if searchString:
        skeleton_code += generate_search_code(searchString)
    return skeleton_code


def generate_request_headers(header_dict):
    """Place the request headers in bash script from header dictionary.

    :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.

    :return: A string of bash code which places headers in the request.
    :rtype:`str`
    """
    skeleton_code = ""
    for key, value in header_dict.items():
        skeleton_code += bash_template.request_header.format(header=str(key), header_value=str(value))

    return skeleton_code


def generate_search_code(searchString):
    """Generate bash code for `searchString` if one is passed.

    :param str searchString: String to be searched for in response to request

    :return: A string of combined bash code for searching given string in response
    :rtype: `str`
    """
    if searchString:
        # Quote single quotes in substring, double quotes are good here
        searchString = re.sub("'", "\\'", searchString)
        return bash_template.code_search.format(search_string=searchString)


def generate_proxy_code(details_dict):
    """Generate bash code for the specific proxy if one is passed.

    :param dict details_dict: Dictionary of request details containing proxy specific information.

    :return: A string of combined bash code for specific proxy
    :rtype: `str`
    """
    if 'proxy_host' and 'proxy_port' in details_dict:
        proxy = details_dict['proxy_host'] + ":" + details_dict['proxy_port']
        return bash_template.proxy_code.format(proxy=proxy)
    else:
        return ""


def generate_body_code(body):
    """Generate bash code for the body of the request if one is passed.

    :param dict details_dict: Dictionary of request details containing data to be sent.

    :return: A string of combined bash code for the body of the request.
    :rtype: `str`
    """
    # Escape single quotes , double quotes are good here
    body = re.sub(r"'", "\\'", body)
    return bash_template.body_code.format(body=str(body))
