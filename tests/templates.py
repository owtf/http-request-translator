code_begin_python = """#!/usr/bin/python
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
    curl_handler.setopt(curl_handler.URL, 'https://google.com/robots.txt')
    curl_handler.setopt(curl_handler.WRITEDATA, buffer)
    curl_handler.setopt(curl_handler.HTTPHEADER, ['Host: google.com'])
    # for verbosity
    curl_handler.setopt(curl_handler.VERBOSE, True)
    # Follow redirects
    curl_handler.setopt(curl_handler.FOLLOWLOCATION, True)
    # For older PycURL versions:
    #curl_handler.setopt(curl_handler.WRITEFUNCTION, buffer.write)
"""


code_search_python = """
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

    match = re.findall(r"hello3131\\"you\\\\"are'awesome", str(response))
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


code_python = """#!/usr/bin/python
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
    curl_handler.setopt(curl_handler.URL, 'https://google.com/robots.txt')
    curl_handler.setopt(curl_handler.WRITEDATA, buffer)
    curl_handler.setopt(curl_handler.HTTPHEADER, ['Host: google.com'])
    # for verbosity
    curl_handler.setopt(curl_handler.VERBOSE, True)
    # Follow redirects
    curl_handler.setopt(curl_handler.FOLLOWLOCATION, True)
    # For older PycURL versions:
    #curl_handler.setopt(curl_handler.WRITEFUNCTION, buffer.write)

    curl_handler.setopt(curl_handler.PROXY, 'http://xyz.com:2223')

    curl_handler.setopt(pycurl.SSL_VERIFYPEER, 1)
    curl_handler.setopt(pycurl.SSL_VERIFYHOST, 2)
    # If providing updated certs
    # curl_handler.setopt(pycurl.CAINFO, "/path/to/updated-certificate-chain.crt")

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

code_post_python = """#!/usr/bin/python
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
    curl_handler.setopt(curl_handler.URL, 'https://www.codepunker.com/tools/http-requests')
    curl_handler.setopt(curl_handler.WRITEDATA, buffer)
    curl_handler.setopt(curl_handler.HTTPHEADER, ['Host: www.codepunker.com'])
    # for verbosity
    curl_handler.setopt(curl_handler.VERBOSE, True)
    # Follow redirects
    curl_handler.setopt(curl_handler.FOLLOWLOCATION, True)
    # For older PycURL versions:
    #curl_handler.setopt(curl_handler.WRITEFUNCTION, buffer.write)

    # Sets request method to POST
    curl_handler.setopt(curl_handler.POSTFIELDS, "extra=whoAreYou")  #expects body to urlencoded

    curl_handler.setopt(pycurl.SSL_VERIFYPEER, 1)
    curl_handler.setopt(pycurl.SSL_VERIFYHOST, 2)
    # If providing updated certs
    # curl_handler.setopt(pycurl.CAINFO, "/path/to/updated-certificate-chain.crt")

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


code_begin_ruby = """require "typhoeus"

url = 'https://google.com/robots.txt'

options = {
    followlocation: true,
    verbose: true,
    method: :get,

    headers: {
    "Host" => " google.com",
    },
"""


code_search_ruby = """
}
req = Typhoeus::Request.new(url, options)
req.on_complete do |response|
  if response.success?
    puts 'Response #{response.code}:'
    begin
        require 'colorize'
        lib_available = true
    rescue LoadError
        lib_available = false
    end

    matched = response.body.match /hello3131\\"you\\\\"are'awesome/

    original = response.body
    if matched then
        if lib_available then
            for i in 0..matched.length
                original.gsub! /#{matched[i]}/, "#{matched[i]}".green
            end
        else
            for i in 0..matched.length
                puts 'Matched item: #{matched[i]}'
            end
        end
    end
    puts original

  elsif response.timed_out?
    puts 'Request Timed Out!'
  elsif response.code == 0
    # Could not get an http response, something's wrong.
    puts response.return_message
  else
    # Received a non-successful http response.
    puts 'HTTP request failed: ' + response.code.to_s
  end
end

req.run
"""


code_ruby = """require "typhoeus"

url = 'https://google.com/robots.txt'

options = {
    followlocation: true,
    verbose: true,
    method: :get,

    headers: {
    "Host" => " google.com",
    },

    proxy: 'http://xyz.com:2223',

}
req = Typhoeus::Request.new(url, options)
req.on_complete do |response|
  if response.success?
    puts 'Response #{response.code}'
    puts response.body

  elsif response.timed_out?
    puts 'Request Timed Out!'
  elsif response.code == 0
    # Could not get an http response, something's wrong.
    puts response.return_message
  else
    # Received a non-successful http response.
    puts 'HTTP request failed: ' + response.code.to_s
  end
end

req.run
"""

code_post_ruby = """require "typhoeus"

url = 'https://www.codepunker.com/tools/http-requests'

options = {
    followlocation: true,
    verbose: true,
    method: :post,

    headers: {
    "Host" => " www.codepunker.com",
    },

    body: "extra=whoAreYou"

}
req = Typhoeus::Request.new(url, options)
req.on_complete do |response|
  if response.success?
    puts 'Response #{response.code}'
    puts response.body

  elsif response.timed_out?
    puts 'Request Timed Out!'
  elsif response.code == 0
    # Could not get an http response, something's wrong.
    puts response.return_message
  else
    # Received a non-successful http response.
    puts 'HTTP request failed: ' + response.code.to_s
  end
end

req.run
"""
code_begin_bash = """#!/usr/bin/env bash
curl"""


code_search_bash = """ | egrep --color " hello3131\\"you\\\\"are'awesome |$" """


code_bash = """#!/usr/bin/env bash
curl -x http://xyz.com:2223 -v --request GET https://google.com/robots.txt  --header "Host: google.com"  --include"""


code_post_bash = """#!/usr/bin/env bash
curl --data "extra=whoAreYou"  -v --request POST https://www.codepunker.com/tools/http-requests  --header "Host: www.codepunker.com"  --include"""

code_begin_php = """if (!extension_loaded('curl')) {
    print 'Curl Extension not found. Exiting';
    exit;
}
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://google.com/robots.txt');
// Set so curl_exec returns the result instead of outputting it.
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
// Set verbosity
curl_setopt($ch, CURLOPT_VERBOSE, 1);
$headers = array();

$headers[] = "Host: google.com";
"""


code_search_php = """
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$response = curl_exec($ch);

if (curl_errno($ch)) {
 print curl_error($ch);
} else {
 curl_close($ch);
}
print $response;
$string = "hello3131\\"you\\\\"are'awesome";
// Blindly copied from http://stackoverflow.com/questions/10778318/test-if-a-string-is-regex
// Checks if the passed string is a regex or a simple string
if( preg_match("/^\/.+\/[a-z]*$/i",$string)) {
    if (preg_match($string, $response, $match)) {
        print 'Found a match!';
    }
}
else {
    if (strpos($response,$string) !== false) {
        print 'Found a match!';
    }
}
"""


code_php = """if (!extension_loaded('curl')) {
    print 'Curl Extension not found. Exiting';
    exit;
}
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://google.com/robots.txt');
// Set so curl_exec returns the result instead of outputting it.
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
// Set verbosity
curl_setopt($ch, CURLOPT_VERBOSE, 1);
$headers = array();

$headers[] = "Host: google.com";

curl_setopt($ch, CURLOPT_PROXY, 'http://xyz.com:2223');

curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$response = curl_exec($ch);

if (curl_errno($ch)) {
 print curl_error($ch);
} else {
 curl_close($ch);
}
print $response;
"""


code_post_php = """if (!extension_loaded('curl')) {
    print 'Curl Extension not found. Exiting';
    exit;
}
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://www.codepunker.com/tools/http-requests');
// Set so curl_exec returns the result instead of outputting it.
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
// Set verbosity
curl_setopt($ch, CURLOPT_VERBOSE, 1);
$headers = array();

$headers[] = "Host: www.codepunker.com";

$content = "extra=whoAreYou";
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $content);

curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$response = curl_exec($ch);

if (curl_errno($ch)) {
 print curl_error($ch);
} else {
 curl_close($ch);
}
print $response;
"""
