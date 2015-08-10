from __future__ import print_function

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from .url import get_url, check_valid_url
from .templates import bash_template


def generate_script(headers, details, search_string=None):
    """Generate the bash script corresponding to the HTTP request.

    :param list headers: Headers list containing fields like 'Host', 'User-Agent', etc.
    :param dict details: Request specific details dictionary like body and method of the request.
    :param str search_string: String to search for in the response to the request. By default remains None.

    :raises ValueError: When url is invalid.

    :return: Generated bash script to send the HTTP request.
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

    # Format basic bash script with proxy and http request.
    skeleton_code = bash_template.begin_code + generate_proxy_code(details) + bash_template.code_simple.format(
        method=details['method'],
        url=url,
        headers=generate_request_headers(headers))
    if method == 'get':
        pass
    elif method == 'post':
        skeleton_code += generate_post_body_code(post_body=details['data'])
    else:
        raise ValueError("'%s' is not supported. Only GET and POST requests are supported yet!" % details['method'])

    if search_string:
        skeleton_code += generate_search_code(search_string)
    return skeleton_code


def generate_request_headers(headers=[]):
    """Generate request headers for the bash script.

    :param list headers: Headers list containing fields like 'Host','User-Agent'.

    :return: Bash script snippet with HTTP requests headers.
    :rtype:`str`
    """
    skeleton_code = ''
    for item in headers:
        header, value = item.split(':', 1)
        skeleton_code += bash_template.request_header.format(
            header=header.replace("'", "\\'"),
            header_value=value.replace("'", "\\'"))
    return skeleton_code


def generate_search_code(search_string=''):
    """Generate search code for the bash script.

    :param str search_string: String to be found in the HTTP response from the server.

    :return: Bash script snippet with the HTTP response search feature.
    :rtype: `str`
    """
    return bash_template.code_search.format(search_string=search_string.replace("'", "\\'"))


def generate_proxy_code(details={}):
    """Generate proxy code for the bash script.

    :param dict details: Dictionary of request details containing proxy specific information.

    :return: Bash script snippet with the proxy code.
    :rtype: `str`
    """
    if 'proxy_host' and 'proxy_port' in details:
        proxy = '%s:%s' % (details['proxy_host'], details['proxy_port'])
        return bash_template.proxy_code.format(proxy=proxy)
    return ''


def generate_post_body_code(post_body=''):
    """Generate body code for the bash script.

    :param str post_body: Body of the request to be sent.

    :return: Bash script snippet with  the body code.
    :rtype: `str`
    """
    return bash_template.post_code.format(post_body=post_body.replace("'", "\\'"))
