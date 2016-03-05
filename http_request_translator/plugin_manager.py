from __future__ import print_function

from .base import AbstractScript
from .script import BashScript, PHPScript, PythonScript, RubyScript


def get_script_class(script_name):
    """Returns the class of the script.

    :param str script_name: language name of the script class which we want to import

    :raises ValueError: When the script is not supported.

    :return: The class of the `script_name` script.
    :rtype: :class:`AbstractScript`
    """
    script_name = script_name.strip().lower()

    for script_class in AbstractScript.__subclasses__():
        if script_name == script_class.__language__:
            return script_class
    raise ValueError("The {} language is not supported.".format(script_name))


def generate_script(script, headers, details, search_string=None):
    """Returns the script code for the HTTP request passed in script language

    :param str script: Name of the language for which script is to be generated
    :param dict headers: Headers information
    :param dict details: Details information
    :param str search_string: string to be searched for in the response for given request

    :return: A combined string of generated code
    :rtype: `str`
    """
    class_script = get_script_class(script.strip().lower())
    return class_script(headers=headers, details=details, search=search_string).generate_script()
