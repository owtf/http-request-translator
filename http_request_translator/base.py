"""

:synopsis: Define the basic script class that will generate the script code.

"""

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
from importlib import import_module

from .url import get_url, check_valid_url


class AbstractScript(object):

    """Abstract representation of a script."""

    __language__ = ''

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
        self.load_attributes(self.__class__)
        self._script = ''
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

        :raises ValueError: when unsupported HTTP method, invalid `headers` or `details` values.

        :return: Generated script code.
        :rtype: str
        """
        self.headers = headers or self.headers
        self.details = details or self.details
        self.search = search or self.search
        if not self.headers:
            raise ValueError("'headers' cannot be equal to '%s'" % self.headers)
        elif not self.details:
            raise ValueError("'details' cannot be equal to '%s'" % self.details)
        if not self.url and self.details:
            self.url = self.encode_url(self.create_url())
        if self.code_begin:
            self._script += self._generate_begin()
        if self.code_proxy:
            self._script += self._generate_proxy()
        method = self.details.get('method', '').strip().lower()
        if method == 'get':
            pass
        elif method == 'post':
            if self.code_post:
                self._script += self._generate_post()
        else:
            raise ValueError("'%s' is not supported! Only GET and POST are supported for now." % self.details['method'])
        if self.code_https:
            self._script += self._generate_https()
        self._script += self._generate_request()
        return self._script

    def _generate_begin(self):
        """Default generation of the beginning of the code.

        :return: Beginning of the code.
        :rtype: str
        """
        return self.code_begin

    def _generate_headers(self):
        """Default generation of request headers.

        :return: Code snippet with HTTP requests headers.
        :rtype: str
        """
        code = ''
        for item in self.headers:
            header, value = item.split(':', 1)
            code += self.code_header.format(header=header.replace('"', '\\"'), value=value.replace('"', '\\"'))
        return code

    def _generate_proxy(self):
        """Default generation of the proxy specific code.

        :return: Code snippet with the proxy information.
        :rtype: str
        """
        if 'proxy_host' in self.details and 'proxy_port' in self.details:
            return self.code_proxy.format(proxy='%s:%s' % (self.details['proxy_host'], self.details['proxy_port']))
        return ''

    def _generate_post(self):
        """Default generation of the post body code.

        :return: Code snippet containing body to be sent in request.
        :rtype: str
        """
        return self.code_post.format(data=self.details.get('data', '').replace('"', '\\"'))

    def _generate_https(self):
        """Default generation of the HTTPS specific code.

        :return: Code snippet with HTTPS setup.
        :rtype: str
        """
        return self.code_https

    def _generate_request(self):
        """Default generation of the request code.

        :return: Code snippet for the request to send.
        :rtype: str
        """
        code = ''
        if self.search:
            if self.code_search:
                code += self._generate_search(self.search)
        else:
            if self.code_nosearch:
                code += self._generate_nosearch()
        return code

    def _generate_search(self, search_string=''):
        """Default generation of the code having search functionality.

        :param str search_string: String to search for in the response to the request.

        :return: Code snippet with the HTTP response search feature.
        :rtype: str
        """
        return self.code_search.format(search_string=search_string.replace('"', '\\"'))

    def _generate_nosearch(self):
        """Default generation of the code having no search functionality.

        :return: Code snippet absent of HTTP response search feature.
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

    @staticmethod
    def load_attributes(cls):
        """Loads attributes to Script class from a given script's template

        Imports the template file/module, assigns all the attributes defined in the template file to the given class.

        :param class cls: Script class to which template is to be loaded.

        :raises AttributeError: When __language__ attribute is not present.
        """
        templates_path = "{}.templates".format(__name__.split('.', 1)[0])
        if not hasattr(cls, '__language__'):
            raise AttributeError("__language__ not found in class: {}, attributes cannot be loaded".format(cls.__name__))
        template = import_module("{templates_path}.{class_template}".format(
            templates_path=templates_path,
            class_template=cls.__language__))
        attributes = (var for var in vars(template) if var.startswith('code_'))
        for attr in attributes:
            setattr(cls, attr, getattr(template, attr))
