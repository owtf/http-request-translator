from __future__ import print_function

import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from url import get_url, check_valid_url
from templates import php_template


def generate_script(header_list, details_dict, searchString=None):
    """Generate the php script for the passed request.

    :param list header_list: Header list containing fields like 'Host','User-Agent'.
    :param dict details_dict: Request specific details like body and method for the request.
    :param str searchString: String to search for in the response to the request. By default remains None.

    :raises ValueError: When url is Invalid

    :return: A combined string of generated code
    :rtype:`str`
    """
    url = get_url(details_dict['Host'], details_dict['pre_scheme'])
    method = details_dict['method']
    url += details_dict['path']
    if not check_valid_url(url):
        raise ValueError("Invalid URL")
    encoding_list = ['HEAD', 'OPTIONS', 'GET']
    if details_dict['data'] and (details_dict['method'] in encoding_list):
        encoded_data = quote(details_dict['data'], '')
        url = url + encoded_data
    skeleton_code = php_template.begin_code.format(url=url)
    skeleton_code += generate_request_headers(header_list)
    if method == "GET":
        pass
    elif method == "POST":
        skeleton_code += php_template.post_request.format(body=generate_body_code(details_dict['data']))
    else:
        print("Only GET and POST requests are supported yet!")
        return ""

    skeleton_code += generate_req_code(details_dict, searchString)

    return skeleton_code


def generate_request_headers(header_list):
    """Place the request headers in php script from header dictionary.

    :param list header_list: Header list containing fields like 'Host','User-Agent'.

    :return: A string of php code which places headers in the request.
    :rtype:`str`
    """
    skeleton_code = ""
    for item in header_list:
        header, value = item.split(":", 1)
        skeleton_code += php_template.request_header.format(header=str(header), header_value=str(value))

    return skeleton_code


def generate_req_code(details_dict, searchString):
    """Generate php code for the body and proxy specific parts of the request.

    :param dict details_dict: Dictionary of request details like proxy,data etc.
    :param str searchString: String to search for in response of the request

    :return: A string of combined php code for specific proxy and searchString if one passed
    :rtype: `str`
    """
    skeleton = ""
    if 'proxy_host' and 'proxy_port' in details_dict:
        skeleton += php_template.proxy_code.format(
            proxy_host=details_dict['proxy_host'], proxy_port=details_dict['proxy_port'])
    skeleton += php_template.req_code
    if searchString:
        searchString = re.sub("'", "\\'", searchString)
        skeleton += php_template.search_code.format(search_string=searchString)
    else:
        skeleton += php_template.non_search_code
    return skeleton


def generate_body_code(body):
    """Generate string for body part of the request.

    :param str body:Passed body of the request

    :return: A formatted string of body code
    :rtype:`str`

    """
    # Escape single quotes , double quotes are good here
    body = re.sub(r"'", "\\'", body)
    return str(body)
