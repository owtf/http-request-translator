import unittest

from http_request_translator import python_script
from .utils import python_generated_search_string, python_generated_script


class TestPythonTranslator(unittest.TestCase):

    def test_generate_search_code(self):
        search_string = "hello3131'you'are'awesome"
        result = python_script.generate_search_code(search_string)
        self.assertEqual(result, python_generated_search_string, 'Invalid generation of python search code')

    def test_generate_proxy_code(self):
        details_dict = {'proxy_port': '2223', 'proxy_host': 'http://xyz.com'}
        result = python_script.generate_proxy_code(details_dict)
        string_generated = """
    c.setopt(c.PROXY, 'http://xyz.com:2223')
"""
        self.assertEqual(result, string_generated, 'Invalid generation of python proxy code')

    def test_generate_script(self):
        header_list = ['Host: google.com']
        details_dict = {'protocol': 'HTTP',
                        'pre_scheme': 'https://',
                        'Host': 'google.com',
                        'version': '1.1',
                        'path': '/robots.txt',
                        'method': 'GET',
                        'data': ''
                        }
        result = python_script.generate_script(header_list, details_dict)
        self.assertEqual(result, python_generated_script, 'Invalid generation of Python script')


if __name__ == '__main__':
    unittest.main()
