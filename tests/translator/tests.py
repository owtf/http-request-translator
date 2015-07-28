import unittest

from http_request_translator import translator


class TestTranslator(unittest.TestCase):

    def test_parse_raw_request_https_domain_no_port(self):
        raw_request = "GET https://google.com/robots.txt HTTP/1.1\n"\
                      "Host: google.com"
        result = translator.parse_raw_request(raw_request)
        self.assertEqual(
            result,
            (
                {'Host': 'google.com'},
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': 'google.com',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET'
                }
            ),
            'Invalid parsing of HTTP request with domain host!')

    def test_parse_raw_request_https_domain_port(self):
        raw_request = "GET https://google.com:31337/robots.txt HTTP/1.1\n"\
                      "Host: google.com:31337"
        result = translator.parse_raw_request(raw_request)
        self.assertEqual(
            result,
            (
                {'Host': 'google.com:31337'},
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': 'google.com:31337',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET'
                }
            ),
            'Invalid parsing of HTTP request with domain host and custom port!')

    def test_parse_raw_request_https_ipv4_no_port(self):
        raw_request = "GET https://127.0.0.1/robots.txt HTTP/1.1\n"\
                      "Host: 127.0.0.1"
        result = translator.parse_raw_request(raw_request)
        self.assertEqual(
            result,
            (
                {'Host': '127.0.0.1'},
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': '127.0.0.1',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET'
                }
            ),
            'Invalid parsing of HTTP request with IPv4 host!')

    def test_parse_raw_request_https_ipv4_port(self):
        raw_request = "GET https://127.0.0.1:31337/robots.txt HTTP/1.1\n"\
                      "Host: 127.0.0.1:31337"
        result = translator.parse_raw_request(raw_request)
        self.assertEqual(
            result,
            (
                {'Host': '127.0.0.1:31337'},
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': '127.0.0.1:31337',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET'
                }
            ),
            'Invalid parsing of HTTP request with IPv4 host and custom port!')

    def test_parse_raw_request_https_ipv6_no_port(self):
        raw_request = "GET https://[::1]/robots.txt HTTP/1.1\n"\
                      "Host: [::1]"
        result = translator.parse_raw_request(raw_request)
        self.assertEqual(
            result,
            (
                {'Host': '[::1]'},
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': '[::1]',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET'
                }
            ),
            'Invalid parsing of HTTP request with IPv6 host!')

    def test_parse_raw_request_https_ipv6_port(self):
        raw_request = "GET https://[::1]:31337/robots.txt HTTP/1.1\n"\
                      "Host: [::1]:31337"
        result = translator.parse_raw_request(raw_request)
        self.assertEqual(
            result,
            (
                {'Host': '[::1]:31337'},
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': '[::1]:31337',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET'
                }
            ),
            'Invalid parsing of HTTP request with IPv6 host and custom port!')


if __name__ == '__main__':
    unittest.main()
