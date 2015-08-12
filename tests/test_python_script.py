import unittest

from http_request_translator import script
from .utils import python_generated_search_string, python_generated_script


class TestPythonTranslator(unittest.TestCase):

    def test_generate_search_code(self):
        search_string = "hello3131'you'are'awesome"
        python_script = script.PythonScript()
        result = python_script._generate_search(search_string)
        self.assertEqual(result, python_generated_search_string, 'Invalid generation of python search code')

    def test_generate_proxy_code(self):
        details = {'protocol': 'HTTP',
                   'pre_scheme': 'https://',
                   'Host': 'google.com',
                   'version': '1.1',
                   'path': '/robots.txt',
                   'method': 'GET',
                   'data': '',
                   'proxy_port': '2223',
                   'proxy_host': 'http://xyz.com'
                   }

        python_script = script.PythonScript(details=details)
        result = python_script._generate_proxy()
        string_generated = """
    c.setopt(c.PROXY, 'http://xyz.com:2223')
"""
        self.assertEqual(result, string_generated, 'Invalid generation of python proxy code')

    def test_generate_script(self):
        headers = ['Host: google.com']
        details = {'protocol': 'HTTP',
                   'pre_scheme': 'https://',
                   'Host': 'google.com',
                   'version': '1.1',
                   'path': '/robots.txt',
                   'method': 'GET',
                   'data': ''
                   }
        python_script = script.PythonScript()
        result = python_script.generate_script(headers, details)
        self.assertEqual(result, python_generated_script, 'Invalid generation of Python script')


if __name__ == '__main__':
    unittest.main()
