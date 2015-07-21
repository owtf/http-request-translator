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
    """Generate URL based on the host.

    :param str host: Host from which to generate the URL (e.g. google.com:443).

    :return: URL with domain and protocol (e.g. https://google.com).
    :rtype: str
    """
    port_protocol = {'443': 'https', '22': 'ssh', '21': 'ftp', '20': 'ftp', '113': 'irc', '80': 'http'}
    protocol = ''
    url = host.strip()
    if ':' in url:  # A port is specified in the domain.
        url, port = url.rsplit(':', 1)
        if port in port_protocol:  # Do we know the protocol?
            protocol = port_protocol[port] + '://'
    protocol = protocol or 'http://'  # Default protocol set to http
    return protocol + url
