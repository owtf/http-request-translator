code_begin = """#!/usr/bin/python
from __future__ import print_function
import re
import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

def main():
    buffer = BytesIO()
    curl_handler = pycurl.Curl()
    curl_handler.setopt(curl_handler.URL, '{url}')
    curl_handler.setopt(curl_handler.WRITEDATA, buffer)
    curl_handler.setopt(curl_handler.HTTPHEADER, {headers})
    # for verbosity
    curl_handler.setopt(curl_handler.VERBOSE, True)
    # Follow redirects
    curl_handler.setopt(curl_handler.FOLLOWLOCATION, True)
    # For older PycURL versions:
    #curl_handler.setopt(curl_handler.WRITEFUNCTION, buffer.write)
"""


code_proxy = """
    curl_handler.setopt(curl_handler.PROXY, '{proxy}')
"""


code_post = """
    # Sets request method to POST
    curl_handler.setopt(curl_handler.POSTFIELDS, "{data}")  #expects body to urlencoded
"""


code_https = """
    curl_handler.setopt(pycurl.SSL_VERIFYPEER, 1)
    curl_handler.setopt(pycurl.SSL_VERIFYHOST, 2)
    # If providing updated certs
    # curl_handler.setopt(pycurl.CAINFO, "/path/to/updated-certificate-chain.crt")
"""


code_search = """
    try:
        curl_handler.perform()
    except pycurl.error, error:
        print('An error occurred: ', error)
    curl_handler.close()

    body = buffer.getvalue()
    # Body is a string on Python 2 and a byte string on Python 3.
    # If we know the encoding, we can always decode the body and
    # end up with a Unicode string.
    response = body.decode('iso-8859-1')

    match = re.findall(r"{search_string}", str(response))
    try:
        from termcolor import colored
        lib_available = True
    except ImportError:
        lib_available = False
    if match:
        for item in match:
            if lib_available:
                replace_string = colored(match[item], 'green')
                response = re.sub(match[item], replace_string, str(response))
            else:
                print("Matched item: ",item)

    print(response)


if __name__ == '__main__':
    main()
"""


code_nosearch = """
    try:
        curl_handler.perform()
    except pycurl.error, error:
        print('An error occurred: ', error)
    curl_handler.close()

    body = buffer.getvalue()
    # Body is a string on Python 2 and a byte string on Python 3.
    # If we know the encoding, we can always decode the body and
    # end up with a Unicode string.
    response = body.decode('iso-8859-1')

    print(response)


if __name__ == '__main__':
    main()
"""
