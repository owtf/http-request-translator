from __future__ import print_function

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from .url import get_url, check_valid_url
from .templates import python_template


def generate_script(headers, details, search_string=None):
    """Generate the python script corresponding to the HTTP request.

    :param list headers: Headers list containing fields like 'Host', 'User-Agent', etc.
    :param dict details: Request specific details dictionary like body and method of the request.
    :param str search_string: String to search for in the response to the request. By default remains None.

    :raises ValueError: When url is invalid.

    :return: Generated python script to send the HTTP request.
    :rtype:`str`
    """
    method = details['method'].lower()
    url = get_url(details['Host'], details['pre_scheme']) + details['path']
    if not check_valid_url(url):
        raise ValueError("Invalid URL '%s'." % url)

    encoding_list = ['head', 'options', 'get']
    if details['data'] and (method in encoding_list):
        encoded_data = quote(details['data'], '')
        url = url + encoded_data

    # Format basic python script with proxy and http request.
    skeleton_code = python_template.begin_code.format(url=url, headers=str(headers)) + generate_proxy_code(details)
    if method == 'get':
        pass
    elif method == 'post':
        skeleton_code += generate_post_body_code(post_body=details['data'])
    else:
        raise ValueError("'%s' is not supported. Only GET and POST requests are supported yet!" % details['method'])

    skeleton_code += generate_https_code(url)
    skeleton_code += generate_search_code(search_string)
    return skeleton_code


def generate_search_code(search_string=''):
    """Generate search code for the python script.

    :param str search_string: String to be found in the HTTP response from the server.

    :return: Python script snippet with the HTTP response search feature.
    :rtype: `str`
    """
    if search_string:
        return python_template.body_code_search.format(search_string=search_string.replace("'", "\\'"))
    return python_template.body_code_simple


def generate_https_code(url):
    """Generate SSL code for the python script.

    :param str url: URL for the request.

    :return: Python script sni[et with the HTTPS setup.
    :rtype:`str`
    """
    if url.startswith('https'):
        return python_template.https_code
    return ''


def generate_proxy_code(details={}):
    """Generate proxy code for the python script.

    :param dict details: Dictionary of request details containing proxy specific information.

    :return: Python script snippet with the proxy code.
    :rtype: `str`
    """
    if 'proxy_host' and 'proxy_port' in details:
        proxy = '%s:%s' % (details['proxy_host'], details['proxy_port'])
        return python_template.proxy_code.format(proxy=proxy)
    return ''


def generate_post_body_code(post_body=''):
    """Generate body code for the python script.

    :param str post_body: Body of the request to be sent.

    :return: Python script snippet with the body code.
    :rtype: `str`
    """
    return python_template.post_code.format(post_body=post_body.replace("'", "\\'"))
