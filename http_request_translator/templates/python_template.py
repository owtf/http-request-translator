begin_code = """
#!/usr/bin/python
from __future__ import print_function
import re
from tornado.httpclient import HTTPRequest, HTTPClient


def main():
"""
proxy_code = """
    headers, url, method = {headers}, '{host}', '{method}'
    body = '{body}'
    proxy_host = '{proxy_host}'
    proxy_port = '{proxy_port}'
    request_object = HTTPRequest(url, method=method, headers=headers, proxy_host=proxy_host,\
        proxy_port=proxy_port, body=body, allow_nonstandard_methods=True)
    response_header = HTTPClient().fetch(request_object).headers
"""

non_proxy_code = """
    headers, url, method = {headers}, '{host}', '{method}'
    body = '{body}'
    request_object = HTTPRequest(url, method=method,headers=headers, body=body, allow_nonstandard_methods=True)
    response_header = HTTPClient().fetch(request_object).headers
"""

body_code_search = """
    match = re.findall(r'{search_string}', str(response_header))
    try:
        from termcolor import colored
        lib_available = True
    except ImportError:
        lib_available = False
    if match:
        for item in match:
            if lib_available:
                replace_string = colored(match[x], 'green')
                response_header = re.sub(match[x], replace_string, str(response_header))
            else:
                print("Matched item: ",item)

    print(response_header)


if __name__ == '__main__':
    main()
"""

body_code_simple = """
    print(response_header)


if __name__ == '__main__':
    main()
"""
