import re

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


def check_valid_url(test_url):
    # TODO: Docstring and comments.
    parsed_url = urlparse(test_url)
    host_address = ''
    if ":" in parsed_url[1]:
        host_address = parsed_url[1].split(':', 1)[0]
    else:
        host_address = parsed_url[1]
    domain_regex = re.compile(
        r'(?:(?:[A-Z](?:[A-Z-]{0,61}[A-Z])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|)',
        re.IGNORECASE)
    domain_match = domain_regex.match(host_address)
    if domain_match:
        if not domain_match.group():
            return False
        else:
            return True
    return False


def get_url(host):
    # TODO: Docstring and comments.
    port_protocol = {443: 'https', 22: 'ssh', 21: 'ftp', 20: 'ftp', 113: 'irc', 80: 'http'}
    url = str(host)
    try:
        port = url.split(':', 2)[1]
        url = url.split(':', 2)[0]
        if int(port.strip()) in port_protocol.keys():
            prefix = str(port_protocol[int(port.strip())]) + "://"
        else:
            prefix = "http://"
    except IndexError:
        prefix = "http://"
    url = prefix + url
    return url
