# -*- coding: utf-8 -*-
import unittest

from http_request_translator import script
from .utils import (python_generated_search_string, python_generated_script,
                    ruby_generated_search_string, ruby_generated_script)


class TestScripts(unittest.TestCase):
    headers = ['Host: google.com']
    details = {'protocol': 'HTTP',
               'pre_scheme': 'https://',
               'Host': 'google.com',
               'version': '1.1',
               'path': '/robots.txt',
               'method': 'GET',
               'proxy_port': '2223',
               'proxy_host': 'http://xyz.com'
               }
    search_string = "hello3131'you'are'awesome"
    ruby_script = script.RubyScript(headers=headers, details=details)
    python_script = script.PythonScript(headers=headers, details=details)
    script_list = [ruby_script, python_script]

    def test_generate_search_code(self):
        for script_name in self.script_list:
            result = script_name._generate_search(self.search_string)
            if (isinstance(script_name, script.RubyScript)):
                to_match = ruby_generated_search_string
            elif (isinstance(script_name, script.PythonScript)):
                to_match = python_generated_search_string

            self.assertEqual(result, to_match, 'Invalid generation of search code for {}'.format(
                script_name.__class__.__name__))

    def test_generate_proxy_code(self):
        for script_name in self.script_list:
            result = script_name._generate_proxy()
            if (isinstance(script_name, script.RubyScript)):
                to_match = """
    proxy: 'http://xyz.com:2223',
"""
            elif (isinstance(script_name, script.PythonScript)):
                to_match = """
    c.setopt(c.PROXY, 'http://xyz.com:2223')
"""
            self.assertEqual(result, to_match, 'Invalid generation of proxy code for {}'.format(
                script_name.__class__.__name__))

    def test_generate_script(self):
        for script_name in self.script_list:
            result = script_name.generate_script()
            if (isinstance(script_name, script.RubyScript)):
                to_match = ruby_generated_script
            elif (isinstance(script_name, script.PythonScript)):
                to_match = python_generated_script
            self.assertEqual(result, to_match, 'Invalid generation of script for {}'.format(
                script_name.__class__.__name__))

    def test_generate_post_code(self):
        self.details['data'] = 'hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:"{}|_+!@#$%^&*()`'
        for script_name in self.script_list:
            result = script_name._generate_post()
            if (isinstance(script_name, script.RubyScript)):
                to_match = """
    body: 'hello7World'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:"{}|_+!@#$%^&*()`'
"""
            elif (isinstance(script_name, script.PythonScript)):
                to_match = """
    # Sets request method to POST
    c.setopt(c.POSTFIELDS, 'hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:"{}|_+!@#$%^&*()`')  #expects body to urlencoded
"""
            self.assertEqual(result, to_match, 'Invalid generation of post code for {}'.format(
                script_name.__class__.__name__))

if __name__ == '__main__':
    unittest.main()
