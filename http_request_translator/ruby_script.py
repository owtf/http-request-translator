from __future__ import print_function

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from .url import check_valid_url, get_url
from .templates import ruby_template


def generate_script(headers, details, search_string=None):
    """Generate the ruby script corresponding to the HTTP request.

    :param list headers: Headers list containing fields like 'Host','User-Agent'.
    :param dict details: Request specific details dictionary like body and method of the request.
    :param str search_string: String to search for in the response to the request. By default remains None.

    :raises ValueError: When Url is invalid or unsupported request method is passed.

    :return: Generated ruby script to send the request.
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

    skeleton_code = ruby_template.begin_code.format(url=url, method=method) + ruby_template.header_code.format(
        headers=generate_request_headers(headers)) + generate_proxy_code(details)
    if method == "get":
        pass
    elif method == "post":
        skeleton_code += generate_post_body_code(post_body=details['data'])
    else:
        raise ValueError("'%s' is not supported. Only GET and POST requests are supported yet!" % details['method'])

    skeleton_code += generate_https_code(url)
    skeleton_code += generate_search_code(search_string)
    return skeleton_code


def generate_request_headers(headers=[]):
    """Place the request headers in ruby script from header dictionary.

    :param list headers: Header list containing fields like 'Host','User-Agent'.

    :return: A string of ruby code which places headers in the request.
    :rtype:`str`
    """
    skeleton_code = ''
    for item in headers:
        header, value = item.split(':', 1)
        skeleton_code += ruby_template.request_header.format(header=str(header), header_value=str(value))
    return skeleton_code


def generate_proxy_code(details={}):
    """Checks if proxy is provided and returns appropriate ruby code.

    :param dict details: Dictionary of request details containing proxy specific information.

    :return: A string of ruby code
    :rtype:`str`
    """
    if 'proxy_host' and 'proxy_port' in details:
        proxy = '%s:%s' % (details['proxy_host'], details['proxy_port'])
        skeleton = ruby_template.proxy_code.format(proxy=proxy)
        return skeleton
    else:
        return ''


def generate_post_body_code(post_body=''):
    """Generate body code for the ruby script.

    :param str post_body: Body of the request to be sent.

    :return: ruby script snippet with the body code.
    :rtype: `str`
    """
    return ruby_template.post_body_code.format(post_body=post_body.replace("'", "\\'"))


def generate_search_code(search_string=''):
    """Generate search code for the ruby script.

    :param str search_string: String to be found in the HTTP response from the server.

    :return: ruby script snippet with the HTTP response search feature.
    :rtype: `str`
    """
    if search_string:
        return ruby_template.body_code_search.format(search_string=search_string.replace("'", "\\'"))
    else:
        return ruby_template.body_code_simple


def generate_https_code(url):
    """Dummy function.

    :param str url: URL for the request.

    :return: Empty String
    :rtype:`str`
    """
    return ''
