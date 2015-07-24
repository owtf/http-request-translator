from __future__ import print_function

import re
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from url import get_url, check_valid_url


def generate_script(header_dict, details_dict, searchString=None):
    """Generate the bash script for the passed request.

    :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.
    :param dict details_dict: Request specific details like body and method for the request.
    :param str searchString: String to search for in the response to the request. By default remains None.

    :raises ValueError: When url is Invalid

    :return: A combined string of generated code
    :rtype:`str`
    """
    method = details_dict['method'].strip()
    url = get_url(header_dict['Host'].strip(), details_dict['pre_scheme'])
    path = details_dict['path']

    if path != "":
        url += path

    encoding_list = ['HEAD', 'OPTIONS', 'GET']

    if details_dict['data'] and (details_dict['method'].strip() in encoding_list):
        encoded_data = quote(details_dict['data'], '')
        url = url + encoded_data

    if not check_valid_url(url):
        raise ValueError("Invalid URL")

    skeleton_code = """
#!/usr/bin/env bash
curl -s --request """
    headers = generate_request_headers(header_dict)
    if method == "GET":
        skeleton_code += generate_proxy_code(details_dict) + generate_request_code(method, url, headers, searchString)

    elif method == "POST":
        skeleton_code += generate_proxy_code(details_dict) + generate_request_code(method, url, headers, searchString)\
                                                           + generate_body_code(details_dict['data'])
    return skeleton_code


def generate_request_headers(header_dict):
    """Place the request headers in bash script from header dictionary.

    :param dict header_dict: Header dictionary containing fields like 'Host','User-Agent'.

    :return: A string of bash code which places headers in the request.
    :rtype:`str`
    """
    skeleton = ""
    for key, value in header_dict.items():
        skeleton += """ --header "%s : %s" """ % (str(key), str(value))

    return skeleton


def generate_request_code(method, url, headers, searchString):
    """Generate bash code for specific `method`, `url`, `headers` and `searchString` if one is passed.

    :param str method: Method of request
    :param str url: Url for request
    :param str headers: Bash specific headers string
    :param str searchString: String to be searched for in response to request

    :return: A string of combined bash code for making request through curl
    :rtype: `str`
    """
    if searchString:
        # Quote single quotes in substring, double quotes are good here
        searchString = re.sub("'", "\\'", searchString)
        return "%s %s %s --include | egrep --color ' %s |$' " % (method, url, headers, searchString)
    else:
        return "%s %s %s --include " % (method, url, headers)


def generate_proxy_code(details_dict):
    """Generate bash code for the specific proxy if one is passed.

    :param dict details_dict: Dictionary of request details containing proxy specific information.

    :return: A string of combined bash code for specific proxy
    :rtype: `str`
    """
    if 'proxy' in details_dict:
        return "-x %s" % (details_dict['proxy'])
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
    return " --data '%s' " % (str(body))
