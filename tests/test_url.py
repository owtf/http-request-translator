import unittest

from http_request_translator import url


class TestURL(unittest.TestCase):

    ###
    # url.check_valid_url
    ###
    def test_check_valid_url(self):
        self.assertTrue(url.check_valid_url("https://github.com:443"))
        self.assertTrue(url.check_valid_url("http://[::1]"))
        self.assertTrue(url.check_valid_url("https://[::1]:443"))

        self.assertFalse(url.check_valid_url("://github.com/"))
        self.assertFalse(url.check_valid_url("https://::1:abcd"))

    ###
    # url.check_valid_port
    ###
    def test_check_valid_port(self):
        self.assertTrue(url.check_valid_port(80))
        self.assertTrue(url.check_valid_port("443"))

        self.assertFalse(url.check_valid_port(909090))
        self.assertFalse(url.check_valid_port("abc"))

    ###
    # url.get_url
    ###
    def test_get_url(self):
        self.assertEqual(url.get_url("github.com:80"), "http://github.com:80")
        self.assertEqual(url.get_url("github.com:443"), "https://github.com:443")
        self.assertEqual(url.get_url("github.com:22"), "ssh://github.com:22")

        self.assertEqual(url.get_url("[::1]:443"), "https://[::1]:443")
