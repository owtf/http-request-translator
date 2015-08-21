# -*- coding: utf-8 -*-
import unittest

from http_request_translator import script
from .templates import (code_begin_python, code_search_python, code_python, code_post_python, code_search_ruby,
                        code_begin_ruby, code_ruby, code_post_ruby, code_begin_bash, code_search_bash, code_bash,
                        code_post_bash, code_search_php, code_php, code_begin_php, code_post_php)


class TestScripts(unittest.TestCase):

    def setUp(self):
        self.headers = ['Host: google.com']
        self.details = {
            'protocol': 'HTTP',
            'pre_scheme': 'https://',
            'Host': 'google.com',
            'version': '1.1',
            'path': '/robots.txt',
            'method': 'GET',
            'proxy_port': '2223',
            'proxy_host': 'http://xyz.com'}
        self.second_headers = ['Host: www.codepunker.com']
        self.second_details = {
            'protocol': 'HTTP',
            'pre_scheme': 'https://',
            'Host': 'www.codepunker.com',
            'version': '1.1',
            'path': '/tools/http-requests',
            'method': 'POST',
            'data': 'extra=whoAreYou'
        }
        self.code_search = """hello3131\"you\\"are'awesome"""
        self.ruby_script = script.RubyScript(headers=self.headers, details=self.details)
        self.python_script = script.PythonScript(headers=self.headers, details=self.details)
        self.bash_script = script.BashScript(headers=self.headers, details=self.details)
        self.php_script = script.PHPScript(headers=self.headers, details=self.details)
        self.script_list = [self.ruby_script, self.python_script, self.bash_script, self.php_script]

    def test_generate_search(self):
        for script_name in self.script_list:
            result = script_name._generate_search(self.code_search)
            if isinstance(script_name, script.RubyScript):
                code_search = code_search_ruby
            elif isinstance(script_name, script.PythonScript):
                code_search = code_search_python
            elif isinstance(script_name, script.BashScript):
                code_search = code_search_bash
            elif isinstance(script_name, script.PHPScript):
                code_search = code_search_php
            self.assertEqual(
                result,
                code_search,
                'Invalid generation of search code for {}'.format(script_name.__class__.__name__))

    def test_generate_proxy(self):
        for script_name in self.script_list:
            result = script_name._generate_proxy()
            if isinstance(script_name, script.RubyScript):
                code_proxy = "\n    proxy: 'http://xyz.com:2223',\n"
            elif isinstance(script_name, script.PythonScript):
                code_proxy = "\n    curl_handler.setopt(curl_handler.PROXY, 'http://xyz.com:2223')\n"
            elif isinstance(script_name, script.BashScript):
                code_proxy = " -x http://xyz.com:2223"
            elif isinstance(script_name, script.PHPScript):
                code_proxy = "\ncurl_setopt($ch, CURLOPT_PROXY, 'http://xyz.com:2223');\n"
            self.assertEqual(
                result,
                code_proxy,
                'Invalid generation of proxy code for {}'.format(script_name.__class__.__name__))

    def test_generate_script(self):
        for script_name in self.script_list:
            result = script_name.generate_script()
            if isinstance(script_name, script.RubyScript):
                code = code_ruby
            elif isinstance(script_name, script.PythonScript):
                code = code_python
            elif isinstance(script_name, script.BashScript):
                code = code_bash
            elif isinstance(script_name, script.PHPScript):
                code = code_php
            self.assertEqual(
                result,
                code,
                'Invalid generation of GET script for {}'.format(script_name.__class__.__name__))

    def test_post_generate_script(self):
        for script_name in self.script_list:
            script_name.url = ''
            result = script_name.generate_script(headers=self.second_headers, details=self.second_details)
            if isinstance(script_name, script.RubyScript):
                code = code_post_ruby
            elif isinstance(script_name, script.PythonScript):
                code = code_post_python
            elif isinstance(script_name, script.BashScript):
                code = code_post_bash
            elif isinstance(script_name, script.PHPScript):
                code = code_post_php
            self.assertEqual(
                result,
                code,
                'Invalid generation of POST script for {}'.format(script_name.__class__.__name__))

    def test_generate_post(self):
        self.details['data'] = 'hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:"{}|_+!@#$%^&*()`'
        for script_name in self.script_list:
            result = script_name._generate_post()
            if isinstance(script_name, script.RubyScript):
                code_post = '\n    body: "hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\\"{}|_+!@#$%^&*()`"\n'
            elif isinstance(script_name, script.PythonScript):
                code_post = '\n    # Sets request method to POST\n    curl_handler.setopt(curl_handler.POSTFIELDS, "hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\\"{}|_+!@#$%^&*()`")  #expects body to urlencoded\n'
            elif isinstance(script_name, script.BashScript):
                code_post = ' --data "hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\\"{}|_+!@#$%^&*()`" '
            elif isinstance(script_name, script.PHPScript):
                code_post = '\n$content = "hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\\"{}|_+!@#$%^&*()`";\ncurl_setopt($ch, CURLOPT_POST, 1);\ncurl_setopt($ch, CURLOPT_POSTFIELDS, $content);\n'
            self.assertEqual(
                result,
                code_post,
                'Invalid generation of post code for {}'.format(script_name.__class__.__name__))

    def test_generate_begin(self):
        for script_name in self.script_list:
            result = script_name._generate_begin()
            if isinstance(script_name, script.RubyScript):
                code_begin = code_begin_ruby
            elif isinstance(script_name, script.PythonScript):
                code_begin = code_begin_python
            elif isinstance(script_name, script.BashScript):
                code_begin = code_begin_bash
            elif isinstance(script_name, script.PHPScript):
                code_begin = code_begin_php
            self.assertEqual(
                result,
                code_begin,
                'Invalid generation of begin code for {}'.format(script_name.__class__.__name__))

    def test_create_url(self):
        for script_name in self.script_list:
            script_name.details['Host'] = 'wrongurl..'
            with self.assertRaises(ValueError):
                script_name.create_url()

    def test_encode_url(self):
        for script_name in self.script_list:
            script_name.details['data'] = "?xx"
            result = script_name.encode_url(script_name.url)
            self.assertEqual(
                result,
                'https://google.com/robots.txt%3Fxx',
                'Invalid generation of begin code for {}'.format(script_name.__class__.__name__))

if __name__ == '__main__':
    unittest.main()
