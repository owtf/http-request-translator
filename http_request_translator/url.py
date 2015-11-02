
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from .util import re_ipv4_address, re_ipv6_address, re_domain


def check_valid_url(url):
    """Verify that a URL (containing the protocol) is valid.

    :param str url: URL containing the protocol to validate.

    :return: ``True`` if `url` is valid, ``False`` otherwise.
    :rtype: bool
    """
    _, netloc, _, _, _, _ = urlparse(url)
    if not netloc:  # No protocol specified and urlparse assumed it was a relative path.
        return False
    if not netloc.startswith('['):  # URL without IPv6 e.g. [::1]
        if ':' in netloc:
            netloc, port = netloc.rsplit(':', 1)
            if port and not check_valid_port(port):
                return False
        if re_ipv4_address.match(netloc):
            return True
        if re_domain.match(netloc):
            return True
    else:
        if not netloc.endswith(']'):  # Is there a port specified? e.g. [::1]:443
            netloc, port = netloc.rsplit(':', 1)
            if port and not check_valid_port(port):
                return False
        if re_ipv6_address.match(netloc[1:-1]):
            return True
    return False


def check_valid_port(port):
    """Verify that a port is valid.

    :param str port: port to validate.

    :return: ``True`` if `port` is valid, ``False`` otherwise.
    :rtype: bool
    """
    try:
        port = int(port)
    except ValueError:
        return False
    if port < 0 or port > 65535:
        return False
    return True


def get_url(host, pre_protocol=None):
    """Generate URL based on the host.

    :param str host: Host from which to generate the URL (e.g. google.com:443).
    :param str pre_protocol: Protocol passed in the GET Path. Example request:
        GET https://127.0.0.1/robots.txt HTTP/1.1
        Host: 127.0.0.1:323
        Then, pre_protocol will be `https`.
        Defaults to `None`.

    :return: URL with domain and protocol (e.g. https://google.com).
    :rtype: str
    """
    port_protocol = {'443': 'https', '22': 'ssh', '21': 'ftp', '20': 'ftp', '113': 'irc', '80': 'http'}
    protocol = ''
    url = host.strip()
    if not url.startswith('['):  # A port is specified in the domain and without IPV6
        if ':' in url:
            _, port = url.rsplit(':', 1)
            if port in port_protocol:  # Do we know the protocol?
                protocol = port_protocol[port] + '://'
    else:
        if not url.endswith(']'):   # IPV6 url with Port, [::1]:443
            _, port = url.rsplit(':', 1)
            if port in port_protocol:  # Do we know the protocol?
                protocol = port_protocol[port] + '://'
    # If GET path already specifies a protocol, give preference to that
    protocol = pre_protocol or protocol or 'http://'  # Default protocol set to http
    return protocol + url
