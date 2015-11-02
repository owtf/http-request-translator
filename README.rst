=======================
HTTP Request Translator
=======================

HTTP Request Translator is a python standalone tool that will help you
translate any raw HTTP requests into the language of your choice.

It supports the following languages:

+ Bash
+ PHP
+ Python
+ Ruby

HTTP Request Translator can be used via its CLI or be imported from your own
python project.

============
Installation
============

HTTP Request Translator can be installed from the ``setup.py`` python script:

1. ``$ git clone https://github.com/owtf/http-request-translator -b dev``
2. ``$ cd ./http-request-translator/``
3. ``$ ./setup.py install``

*Note*: The last step might require root privileges.

=====
Usage
=====

Command Line Interface
======================

HTTP Request Translator provides a complete command line interface (CLI) to
make it easy for you to use it.

1. Translate a raw request from the CLI to a single script: ``$ http_request_translator -o python -r "<Your request>"``
2. Specify multiple scripts: ``$ http_request_translator -o python,bash,ruby -r "<Your Request>"``
3. Pass data along with the request: ``$ http_request_translator -o <your favorite script(s)> -d "<body/url parameters to be sent>" -r "Your Request"``
4. Specify a proxy server for sending request: ``$ http_request_translator -o <your favorite script(s)> -p "proxy_url:proxy_port" -r "Your Request"``
5. Search the response by either using the regex-search or simple string search *(but not both)*.
    + For simple string search: ``$ http_request_translator -ss "some_string" -r "Your Request" -o <your favorite script(s)>``
    + For regex search: ``$ http_request_translator -se "some_regex" -r "Your Request" -o <your favorite script(s)>``
6. Manually enter the request using interactive mode: ``$ http_request_translator -o <your favorite script(s)> -i``
7. Specify a file to read the request from: ``$ http_request_translator -f some_file -o <your favorite script(s)>``

See ``--help`` or ``-h`` for the exhaustive list of available options.
