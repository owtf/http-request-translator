try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

from .plugin_manager import generate_script


class HttpRequestTranslator(object):
    """Main Interface for the tool.
    """

    def __init__(self, languages=['bash'], request=None, headers=None, details=None, proxy=None, search_string='',
        regex=None):
        self.languages = languages
        self.request = request
        self.headers = headers
        self.details = details
        self.proxy = proxy
        self.search_string = search_string
        self.regex = regex

    def generate_code(self):
        """Generates code for all the languages defined in the object.

        :return: A dictionary of language name and respective code.
        :rtype: dict
        """
        self._parse_request()
        all_code = {}
        for language in self.languages:
            all_code[language] = generate_script(language, self.headers, self.details, self.search_string)
        return all_code

    def _parse_request(self):
        """Parses Raw HTTP request into separate dictionaries for headers and body and other parameters.

        :param str request: Raw HTTP request.

        :raises ValueError: When request passed in malformed.

        :return: A tuple of two dictionaries where the first one is the headers and the second the details.
        :rtype: tuple
        """
        headers_lines = self.request.splitlines()
        if not headers_lines:
            raise ValueError("Request Malformed. Please Enter a Valid HTTP request.")
        new_request_method = headers_lines.pop(0)
        # Headers
        header_list = []
        while headers_lines:
            line = headers_lines.pop(0)
            if not line.strip('\r\n'):  # Empty line? Therefore the headers are over and the content is starting.
                break
            header_list.append(line)
            try:
                header, value = line.split(":", 1)
            except IndexError:
                raise ValueError("Headers Malformed. Please Enter a Valid HTTP request.")
            if header.lower() == "host":
                host = value.strip()  # Keep hostname for further checks
        # Data
        data = ''
        if headers_lines:
            data = ''.join(headers_lines)
        # Details
        details_dict = {}
        details_dict['data'] = data
        details_dict['method'] = new_request_method.split(' ', 1)[0].strip()
        details_dict['Host'] = host
        # Not using whatever stored in parsed_request for the reason to keep the request as original as possible
        try:  # try to split the path from request if one is passed.
            proto_ver = new_request_method.split(' ', 2)[2].split('/', 1)
            details_dict['protocol'] = proto_ver[0].strip()
            details_dict['version'] = proto_ver[1].strip()
            details_dict['path'] = new_request_method.split(' ', 2)[1].strip()
        except IndexError:
            details_dict['path'] = ""
            try:
                proto_ver = new_request_method.split(' ', 2)[1].split('/', 1)
            except IndexError:  # Failed to get protocol and version.
                raise ValueError("Request Malformed. Please Enter a Valid HTTP request.")
            details_dict['protocol'] = proto_ver[0].strip()
            details_dict['version'] = proto_ver[1].strip()
        # Parse the GET Path to update it to only contain the relative path and not whole url
        # scheme://netloc/path;parameters?query#fragment
        # Eg: Path=https://google.com/robots.txt to /robots.txt
        scheme, netloc, path, params, query, frag = urlparse(details_dict['path'])
        if params:
            path = path + ";" + params
        if query:
            path = path + "?" + query
        if frag:
            path = path + "#" + frag
        details_dict['path'] = path
        # If scheme is specified in GET Path and Header 'Host' Field doesn't already starts with it
        if scheme and not host.startswith(scheme):
            details_dict['pre_scheme'] = scheme + "://"  # Store the scheme defined in GET path for later checks
        else:
            details_dict['pre_scheme'] = ''
        # Assign header list and details dict
        self.headers = header_list
        self.details = details_dict
