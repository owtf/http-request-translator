# -*- coding: utf-8 -*-
import unittest

from http_request_translator import script
from .templates import (code_search_python, code_python,
    code_search_ruby, code_ruby)


class TestScripts(unittest.TestCase):

    def setUp(self):
        self.headers = ['Host: google.com']
        self.details = {'protocol': 'HTTP',
            'pre_scheme': 'https://',
            'Host': 'google.com',
            'version': '1.1',
            'path': '/robots.txt',
            'method': 'GET',
            'proxy_port': '2223',
            'proxy_host': 'http://xyz.com'}

        self.code_search = "hello3131'you'are'awesome"
        self.ruby_script = script.RubyScript(headers=self.headers, details=self.details)
        self.python_script = script.PythonScript(headers=self.headers, details=self.details)
        self.script_list = [self.ruby_script, self.python_script]

    def test_generate_search(self):
        for script_name in self.script_list:
            result = script_name._generate_search(self.code_search)
            if (isinstance(script_name, script.RubyScript)):
                code_search = code_search_ruby
            elif (isinstance(script_name, script.PythonScript)):
                code_search = code_search_python

            self.assertEqual(result, code_search, 'Invalid generation of search code for {}'.format(
                script_name.__class__.__name__))

    def test_generate_proxy(self):
        for script_name in self.script_list:
            result = script_name._generate_proxy()
            if (isinstance(script_name, script.RubyScript)):
                code_proxy = "\n    proxy: 'http://xyz.com:2223',\n"
            elif (isinstance(script_name, script.PythonScript)):
                code_proxy = "\n    c.setopt(c.PROXY, 'http://xyz.com:2223')\n"
            self.assertEqual(result, code_proxy, 'Invalid generation of proxy code for {}'.format(
                script_name.__class__.__name__))

    def test_generate_script(self):
        for script_name in self.script_list:
            result = script_name.generate_script()
            if (isinstance(script_name, script.RubyScript)):
                code = code_ruby
            elif (isinstance(script_name, script.PythonScript)):
                code = code_python
            self.assertEqual(result, code, 'Invalid generation of script for {}'.format(
                script_name.__class__.__name__))

    def test_generate_post(self):
        self.details['data'] = 'hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:"{}|_+!@#$%^&*()`'
        for script_name in self.script_list:
            result = script_name._generate_post()
            if (isinstance(script_name, script.RubyScript)):
                code_post = "\n    body: 'hello7World'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\"{}|_+!@#$%^&*()`'\n"
            elif (isinstance(script_name, script.PythonScript)):
                code_post = "\n    # Sets request method to POST\n    c.setopt(c.POSTFIELDS, 'hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\"{}|_+!@#$%^&*()`')  #expects body to urlencoded\n"
            self.assertEqual(result, code_post, 'Invalid generation of post code for {}'.format(
                script_name.__class__.__name__))

if __name__ == '__main__':
    unittest.main()
