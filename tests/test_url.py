import unittest

from hrt import url


class TestURL(unittest.TestCase):

    ###
    # url.check_valid_url
    ###
    def test_check_valid_url(self):
        self.assertTrue(url.check_valid_url("https://github.com:443"))
        self.assertTrue(url.check_valid_url("http://[::1]"))
        self.assertTrue(url.check_valid_url("https://[::1]:443"))
        self.assertTrue(url.check_valid_url("http://" + 'a' * 63 + ".com"))
        self.assertTrue(url.check_valid_url("http://192.168.1.1"))

        self.assertFalse(url.check_valid_url("://github.com/"))
        self.assertFalse(url.check_valid_url("https://::1:abcd"))
        self.assertFalse(url.check_valid_url("http://" + 'a' * 64 + ".com"))
        self.assertFalse(url.check_valid_url("http://192.999.1.1"))
        self.assertFalse(url.check_valid_url("https://[::1]:invalid"))
        self.assertFalse(url.check_valid_url("https://[::1]:9999999999"))

        # Regression for https://github.com/owtf/http-request-translator/issues/44
        self.assertTrue(url.check_valid_url("http://www.cmd5.com"))
        self.assertTrue(url.check_valid_url("https://www-cmd5.com"))

        # Regression for https://github.com/owtf/http-request-translator/issues/59
        self.assertTrue(url.check_valid_url('http://9gag.com'))
        self.assertTrue(url.check_valid_url('https://9gag.com'))
        self.assertTrue(url.check_valid_url('http://gag9.com'))
        self.assertTrue(url.check_valid_url('https://gag9.com'))

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
