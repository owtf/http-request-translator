"""

:synopsis: Define the basic script class that will generate the script code.

"""

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from .url import get_url, check_valid_url


class AbstractScript(object):

    """Abstract representation of a script."""

    code_begin = ''
    code_header = ''
    code_proxy = ''
    code_post = ''
    code_https = ''
    code_search = ''
    code_nosearch = ''

    def __init__(self, headers=None, details=None, search=None):
        """Initialize the script generation.

        :param list headers: Headers list containing fields like 'Host', 'User-Agent', etc.
        :param dict details: Request specific details dictionary like body and method of the request.
        :param str search: String to search for in the response to the request.

        :raises ValueError: When url is invalid.
        """
        self.script = ''
        self.headers = headers
        self.details = details
        self.search = search
        self.url = ''
        if self.details:
            self.url = self.encode_url(self.create_url())

    def generate_script(self, headers=None, details=None, search=None):
        """Generate script code.

        :param list headers: Headers list containing fields like 'Host', 'User-Agent', etc.
        :param dict details: Request specific details dictionary like body and method of the request.
        :param str search: String to search for in the response to the request.

        :raises ValueError: when unsupported HTTP method.

        :return: Generated script code.
        :rtype: str
        """
        self.headers = headers or self.headers
        self.details = details or self.details
        self.search = search or self.search
        if not self.url and self.details:
            self.url = self.encode_url(self.create_url())
        if self.code_begin:
            self.script += self._generate_begin()
        if self.code_proxy:
            self.script += self._generate_proxy()
        method = self.details.get('method', '').strip().lower()
        if method == 'get':
            pass
        elif method == 'post':
            if self.code_post:
                self.script += self._generate_post()
        else:
            raise ValueError("'%s' is not supported. Only GET and POST requests are supported yet!" % details['method'])
        if self.code_https:
            self.script += self._generate_https()
        self.script += self._generate_request()
        return self.script

    def _generate_begin(self):
        """Default generation of the beginning of the code.

        :return: Beginning of the code.
        :rtype: str
        """
        return self.code_begin

    def _generate_headers(self):
        """Default generation of the headers of the code.

        :return: Headers of the code.
        :rtype: str
        """
        code = ''
        for item in self.headers:
            header, value = item.split(':', 1)
            code += self.code_header.format(header=header.replace("'", "\\'"), value=value.replace("'", "\\'"))
        return code

    def _generate_proxy(self):
        """Default generation of the proxy of the code.

        :return: Proxy of the code.
        :rtype: str
        """
        if 'proxy_host' in self.details and 'proxy_port' in self.details:
            return self.code_proxy.format(proxy='%s:%s' % (self.details['proxy_host'], self.details['proxy_port']))
        return ''

    def _generate_post(self):
        """Default generation of the post of the code.

        :return: Post of the code.
        :rtype: str
        """
        return self.code_post.format(data=self.details.get('data', ''))

    def _generate_https(self):
        """Default generation of the HTTPS of the code.

        :return: HTTPS of the code.
        :rtype: str
        """
        return self.code_https

    def _generate_request(self):
        """Default generation of the request of the code.

        :return: Request of the code.
        :rtype: str
        """
        code = ''
        if self.search:
            if self.code_search:
                code += self._generate_search()
        else:
            if self.code_nosearch:
                code += self._generate_nosearch()
        return code

    def _generate_search(self):
        """Default generation of the search of the code.

        :return: Search of the code.
        :rtype: str
        """
        return self.code_search

    def _generate_nosearch(self):
        """Default generation of the no search of the code.

        :return: No search of the code.
        :rtype: str
        """
        return self.code_nosearch

    def create_url(self):
        """Create valid URL.

        :raises ValueError: When URL is invalid.

        :return: Created URL.
        :rtype: str
        """
        url = get_url(self.details.get('Host', ''), self.details.get('pre_scheme', '')) + self.details.get('path', '')
        if not check_valid_url(url):
            raise ValueError("Invalid URL '%s'." % url)
        return url

    def encode_url(self, url):
        """Check if the URL of the HTTP request needs encoding.

        :param str url: URL to encode if needed.

        :return: Encoded URL if encoding is needed.
        :rtype: str
        """
        http_verb_with_encoding = ['head', 'options', 'get']
        encoded_url = url
        if self.details.get('data') and (self.details.get('method', '').lower() in http_verb_with_encoding):
            encoded_url += quote(self.details['data'], '')
        return encoded_url
