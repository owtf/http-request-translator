from __future__ import print_function

import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from .url import check_valid_url, get_url
from .templates import ruby_template


def generate_script(header_list, details_dict, searchString=None):
    """Generate the ruby script for the passed request.

    :param list header_list: Header list containing fields like 'Host','User-Agent'.
    :param dict details_dict: Request specific details like body and method for the request.
    :param str searchString: String to search for in the response to the request. By default remains None.

    :raises ValueError: When Url is Invalid

    :return: A combined string of generated code
    :rtype:`str`
    """
    method = details_dict['method']
    url = get_url(details_dict['Host'], details_dict['pre_scheme'])
    url += details_dict['path']

    encoding_list = ['HEAD', 'OPTIONS', 'GET']

    if details_dict['data'] and (details_dict['method'] in encoding_list):
        encoded_data = quote(details_dict['data'], '')
        url = url + encoded_data

    if not check_valid_url(url):
        raise ValueError("Invalid URL")

    skeleton_code = ruby_template.begin_code.format(method=method)
    skeleton_code += ruby_template.header_code.format(headers=generate_request_headers(header_list))
    skeleton_code += generate_proxy_code(details_dict)
    if method == "GET":
        pass

    elif method == "POST":
        body = details_dict['data']
        skeleton_code += ruby_template.post_body_code.format(body=generate_body_code(body))
    else:
        print("Only GET and POST requests are supported yet!")
        return ""

    if searchString:
        skeleton_code += ruby_template.body_code_search.format(url=url, search_string=searchString)
    else:
        skeleton_code += ruby_template.body_code_simple.format(url=url)
    return skeleton_code


def generate_request_headers(header_list):
    """Place the request headers in ruby script from header dictionary.

    :param list header_list: Header list containing fields like 'Host','User-Agent'.

    :return: A string of ruby code which places headers in the request.
    :rtype:`str`
    """
    skeleton_code = ""
    for item in header_list:
        header, value = item.split(":", 1)
        skeleton_code += ruby_template.request_header.format(header=str(header), header_value=str(value))
    return skeleton_code


def generate_proxy_code(details_dict):
    """Checks if proxy is provided and returns appropriate ruby code.

    :param dict details_dict: Dictionary of request details containing proxy specific information.

    :return: A string of ruby code
    :rtype:`str`
    """
    if 'proxy_host' and 'proxy_port' in details_dict:
        skeleton = ruby_template.proxy_code.format(
            proxy_host=details_dict['proxy_host'], proxy_port=details_dict['proxy_port'])
        return skeleton
    else:
        return ""


def generate_body_code(body):
    """Generate string for body part of the request.

    :param str body:Passed body of the request

    :return: A formatted string of body code
    :rtype:`str`

    """
    # Escape single quotes , double quotes are good here
    body = re.sub(r"'", "\\'", body)
    return str(body)
