from __future__ import print_function

import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from .url import get_url, check_valid_url
from .templates import python_template


def generate_script(header_list, details_dict, searchString=None):
    """Generate the python script for the passed request.

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
    skeleton_code = python_template.begin_code.format(url=url, header_list=str(header_list))
    skeleton_code += generate_proxy_code(details_dict)
    if method == "GET":
        pass
    elif method == "POST":
        if details_dict['data']:
            # Escape single quotes , double quotes are good here
            body = re.sub(r"'", "\\'", details_dict['data'])
        else:
            body = ""
        skeleton_code += python_template.post_code.format(post_body=body)

    else:
        print("Only GET and POST requests are supported yet!")
        return ""

    skeleton_code += generate_https_code(url)
    skeleton_code += generate_search_code(searchString)
    return skeleton_code


def generate_proxy_code(details_dict):
    """Generate python code for proxy specific parts of the request.

    :param dict details_dict: Dictionary of request details like proxy,data etc.

    :return: A string of combined python code for specific proxy if one passed
    :rtype: `str`
    """

    if 'proxy_host' and 'proxy_port' in details_dict:
        return python_template.proxy_code.format(
            proxy_host=details_dict['proxy_host'], proxy_port=details_dict['proxy_port'])
    else:
        return ""


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


def generate_https_code(url):
    """Checks if url is 'https' and returns appropriate python code.

    :param str url: Url for the request

    :return: A string of python code
    :rtype:`str`
    """
    if url.startswith('https'):
        return python_template.https_code
    else:
        return ""
