from __future__ import print_function

import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from url import get_url, check_valid_url
from templates import python_template


def generate_script(header_dict, details_dict, searchString=None):
    """Generate the python script for the passed request.

    :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.
    :param dict details_dict: Request specific details like body and method for the request.
    :param str searchString: String to search for in the response to the request. By default remains None.

    :raises ValueError: When url is Invalid

    :return: A combined string of generated code
    :rtype:`str`
    """
    url = get_url(header_dict['Host'], details_dict['pre_scheme'])
    method = details_dict['method'].strip()
    if details_dict['path'] != "":
        url += details_dict['path']
    if not check_valid_url(url):
        raise ValueError("Invalid URL")
    encoding_list = ['HEAD', 'OPTIONS', 'GET']
    if details_dict['data'] and (details_dict['method'].strip() in encoding_list):
        encoded_data = quote(details_dict['data'], '')
        url = url + encoded_data
    skeleton_code = python_template.begin_code
    if method == "GET":
        skeleton_code += generate_req_code(header_dict, details_dict, url) + generate_search_code(searchString)
    elif method == "POST":
        skeleton_code += generate_req_code(header_dict, details_dict, url) + generate_search_code(searchString)
    return skeleton_code


def generate_req_code(header_dict, details_dict, url):
    """Generate python code for the body and proxy specific parts of the request.

    :param dict header_dict: Dictionary of request headers.
    :param dict details_dict: Dictionary of request details like proxy,data etc.
    :param str url: URL for the request.

    :raises IndexError: If proxy provided is invalid

    :return: A string of combined python code for specific proxy if one passed
    :rtype: `str`
    """
    if details_dict['data']:
        # Escape single quotes , double quotes are good here
        body = re.sub(r"'", "\\'", details_dict['data'])
    else:
        body = ""

    if 'proxy' in details_dict:
        try:
            proxy_host, proxy_port = details_dict['proxy'].split(':')
        except IndexError:
            raise IndexError("Proxy provided is invalid.")
        return python_template.proxy_code.format(headers=str(header_dict),
                                                 host=url,
                                                 method=details_dict['method'].strip(),
                                                 proxy_host=proxy_host,
                                                 proxy_port=proxy_port,
                                                 body=str(body))
    else:
        return python_template.non_proxy_code.format(headers=str(header_dict),
                                                     host=url,
                                                     method=details_dict['method'].strip(),
                                                     body=str(body))


def generate_search_code(searchString):
    """Generate python code to match the searchString in the response of given request.

    :param str searchString: String to be searched for in response to request.

    :return: A string of python code for searching the passed string in response.
    :rtype: `str`
    """
    if searchString:
        searchString = re.sub("'", "\\'", searchString)
        return python_template.body_code_search.format(search_string=searchString)
    else:
        return python_template.body_code_simple
