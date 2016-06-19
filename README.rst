=======================
HTTP Request Translator
=======================

.. image:: https://travis-ci.org/owtf/http-request-translator.svg?branch=dev
    :target: https://travis-ci.org/owtf/http-request-translator

HTTP Request Translator is a python standalone tool that will help you
translate any raw HTTP requests into the language of your choice.

It supports the following languages:

+ Bash
+ PHP
+ Python
+ Ruby

HTTP Request Translator can be used via its CLI or be imported from your own
python project (actively supported version 2.7 and 3.3+).

============
Installation
============

1. ``$ git clone https://github.com/owtf/http-request-translator``
2. ``$ cd ./http-request-translator/``
3. ``$ make install``

*Note*: The last step might require root privileges.

=====
Usage
=====

Command Line Interface
======================

HTTP Request Translator provides a complete command line interface (CLI) to
make it easy for you to use it.

.. code-block:: bash

    usage: hrt [-h] [--language LANGUAGE] [--proxy [PROXY]]
                                   [--search_string SEARCH_STRING | --search_regex SEARCH_REGEX]
                                   [--interactive] [--data DATA]
                                   [--request REQUEST | --file FILE]

    Request Translator is a standalone tool that can translate raw HTTP requests
    into bash/python/php/ruby scripts

    optional arguments:
      -h, --help            show this help message and exit
      --language LANGUAGE, -l LANGUAGE
                            Generates a script in language 'language' for given
                            HTTP request. If you want to generate multiple
                            scripts, separate the script's name with a <,>.
                            Available languages: bash, php, python, ruby
      --proxy [PROXY], -p [PROXY]
                            Generates command/script with relevant, specified
                            proxy
      --search_string SEARCH_STRING, -ss SEARCH_STRING
                            Sends the request and searches for the required string
                            in the response (i.e literal match)
      --search_regex SEARCH_REGEX, -se SEARCH_REGEX
                            Sends the request and searches for the required regex
                            in the response (i.e regex match)
      --interactive, -i     Interactive mode: read raw HTTP request from keyboard,
                            hit enter when ready. Type 'Ctrl+D' or 'Ctrl+C'to exit
                            from the interactive mode.
      --data DATA, -d DATA  Add the data that you want to send along with the
                            header
      --request REQUEST, -r REQUEST
                            Input the HTTP request
      --file FILE, -f FILE  Input file for HTTP request
