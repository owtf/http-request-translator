from __future__ import print_function

import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from url import check_valid_url, get_url
from templates import ruby_template


def generate_script(header_dict, details_dict, searchString=None):
    """Generate the ruby script for the passed request.

    :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.
    :param dict details_dict: Request specific details like body and method for the request.
    :param str searchString: String to search for in the response to the request. By default remains None.

    :raises ValueError: When Url is Invalid

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

    skeleton_code = ruby_template.begin_code.format(host=url)

    if method == "GET":
        skeleton_code += ruby_template.get_request
        skeleton_code += generate_request_headers(header_dict)
        skeleton_code += generate_proxy_code(details_dict)
        skeleton_code += generate_https_code(url)

    elif method == "POST":
        body = details_dict['data']
        skeleton_code += ruby_template.post_request.format(body=generate_body_code(body))
        skeleton_code += generate_request_headers(header_dict)
        skeleton_code += generate_proxy_code(details_dict)
        skeleton_code += generate_https_code(url)

    if searchString:
        skeleton_code += ruby_template.body_code_search.format(search_string=searchString)
    else:
        skeleton_code += ruby_template.body_code_simple
    return skeleton_code


def generate_request_headers(header_dict):
    """Place the request headers in ruby script from header dictionary.

    :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.

    :return: A string of ruby code which places headers in the request.
    :rtype:`str`
    """
    skeleton = ""
    for key, value in header_dict.items():
        skeleton_ = ruby_template.request_header.format(header=str(key), header_value=str(value))
        skeleton += skeleton_
    return skeleton


def generate_https_code(url):
    """Checks if url is 'https' and returns appropriate ruby code.

    :param str url: Url for the request

    :return: A string of ruby code
    :rtype:`str`
    """
    if url.startswith('https'):
        return ruby_template.https_code
    else:
        return ""


def generate_proxy_code(details_dict):
    """Checks if proxy is provided and returns appropriate ruby code.

    :param dict details_dict: Dictionary of request details containing proxy specific information.

    :raises IndexError: When proxy provided is invalid

    :return: A string of ruby code
    :rtype:`str`
    """
    if 'proxy' in details_dict:
        try:
            proxy_host, proxy_port = details_dict['proxy'].split(':')
            skeleton = ruby_template.proxy_code.format(proxy_host=proxy_host.strip(), proxy_port=proxy_port.strip())
            return skeleton
        except IndexError:
            raise IndexError("Proxy provided is invalid.")
    else:
        return ruby_template.non_proxy_code


def generate_body_code(body):
    """Generate string for body part of the request.

    :param str body:Passed body of the request

    :return: A formatted string of body code
    :rtype:`str`

    """
    # Escape single quotes , double quotes are good here
    body = re.sub(r"'", "\\'", body)
    return str(body)
