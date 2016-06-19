========================
HTTP Request Translator
========================

HTTP request translator is a *standalone* *tool* that can:

* Be used from inside OR outside of OWTF.

* Translate raw HTTP requests to bash/python/php/ruby scripts

* Provide essential quick and dirty transforms: base64(encode/decode), urlencode(encode/decode)

Installation
=============

Currently the only installation method is to install from source. However it will be available as a library from PyPI.

The first step is to clone the repository:

.. code-block:: bash

    $ git clone https://github.com/owtf/http-request-translator.git

Then run the setup.py script:

.. code-block:: bash

    $ ./setup.py install

It is recommended to install in a `virtualenv`.

Usage
=============

To translate a raw request from the CLI to a single script:

.. code-block:: bash

    $ hrt -o python -r "<Your request>"

If you want to specify multiple scripts:

.. code-block:: bash

    $ hrt -o python,bash,ruby -r "<Your Request>"

If you want to pass data along with the request:

.. code-block:: bash

    $ hrt -o <your favorite script(s)> -d "<body/url parameters to be sent>" -r "Your Request"

If you want to specify a proxy server for sending request:

.. code-block:: bash

    $ hrt -o <your favorite script(s)> -p "proxy_url:proxy_port" -r "Your Request"

You can search the response by either using the regex-search or simple string search *(but not both)*.

For simple string search:

.. code-block:: bash

    $ hrt -ss "some_string" -r "Your Request" -o <your favorite script(s)>

For regex search:

.. code-block:: bash

    $ hrt -se "some_regex" -r "Your Request" -o <your favorite script(s)>

If you want to manually enter the request, use `-i` option:

.. code-block:: bash

    $ hrt -o <your favorite script(s)> -i

If you want to specify a file to read the request from, then do:

.. code-block:: bash

    $ hrt -f some_file -o <your favorite script(s)>

See `--help` or `-h` for more details.
