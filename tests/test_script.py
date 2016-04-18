# -*- coding: utf-8 -*-
import unittest

from http_request_translator.base import AbstractScript
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

        self.script_list = []
        for script_class in AbstractScript.__subclasses__():
            self.script_list.append(script_class(headers=self.headers, details=self.details))

    def test_generate_search(self):
        for script_name in self.script_list:
            result = script_name._generate_search(self.code_search)
            self.assertEqual(
                result,
                globals()["code_search_" + script_name.__language__],
                'Invalid generation of search code for {}'.format(script_name.__class__.__name__))

    def test_generate_proxy(self):
        code_proxy = {
            'bash': " -x http://xyz.com:2223",
            'php': "\ncurl_setopt($ch, CURLOPT_PROXY, 'http://xyz.com:2223');\n",
            'python': "\n    curl_handler.setopt(curl_handler.PROXY, 'http://xyz.com:2223')\n",
            'ruby': "\n    proxy: 'http://xyz.com:2223',\n"}
        for script_name in self.script_list:
            result = script_name._generate_proxy()
            self.assertEqual(
                result,
                code_proxy[script_name.__language__],
                'Invalid generation of proxy code for {}'.format(script_name.__class__.__name__))

    def test_generate_script(self):
        for script_name in self.script_list:
            result = script_name.generate_script()
            self.assertEqual(
                result,
                globals()["code_" + script_name.__language__],
                'Invalid generation of GET script for {}'.format(script_name.__class__.__name__))

    def test_post_generate_script(self):
        for script_name in self.script_list:
            script_name.url = ''
            result = script_name.generate_script(headers=self.second_headers, details=self.second_details)
            self.assertEqual(
                result,
                globals()["code_post_" + script_name.__language__],
                'Invalid generation of POST script for {}'.format(script_name.__class__.__name__))

    def test_generate_post(self):
        code_post = {
            'bash': ' --data "hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\\"{}|_+!@#$%^&*()`" ',
            'php': '\n$content = "hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\\"{}|_+!@#$%^&*()`";\ncurl_setopt($ch, CURLOPT_POST, 1);\ncurl_setopt($ch, CURLOPT_POSTFIELDS, $content);\n',
            'python': '\n    # Sets request method to POST\n    curl_handler.setopt(curl_handler.POSTFIELDS, "hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\\"{}|_+!@#$%^&*()`")  #expects body to urlencoded\n',
            'ruby': '\n    body: "hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:\\"{}|_+!@#$%^&*()`"\n'}
        self.details['data'] = 'hello7World\'Ω≈ç√∫˜µ≤≥÷田中さんにあげて下さい,./;[]\-=<>?:"{}|_+!@#$%^&*()`'
        for script_name in self.script_list:
            result = script_name._generate_post()
            self.assertEqual(
                result,
                code_post[script_name.__language__],
                'Invalid generation of post code for {}'.format(script_name.__class__.__name__))

    def test_generate_begin(self):
        for script_name in self.script_list:
            result = script_name._generate_begin()
            self.assertEqual(
                result,
                globals()["code_begin_" + script_name.__language__],
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
