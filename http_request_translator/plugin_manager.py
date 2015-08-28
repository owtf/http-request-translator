from __future__ import print_function

from .script import BashScript, PHPScript, PythonScript, RubyScript


def hardcoded_script_import(script_name):
    """Manually find the class of the script.

    :param str script_name: Name of the script from which to import the function.

    :raises ValueError: When the script is not supported.

    :return: The class of the `script_name` script.
    :rtype: :class:`AbstractScript`
    """
    if script_name == 'bash':
        return BashScript
    elif script_name == 'php':
        return PHPScript
    elif script_name == 'python':
        return PythonScript
    elif script_name == 'ruby':
        return RubyScript
    raise ValueError("The '%s' language is not supported yet." % script_name)


def plugin_manager(script_list, parsed_tuple, search_string=None):
    # TODO: Docstring and comments.
    default = len(script_list) or False
    for script in script_list:
        class_script = hardcoded_script_import(script.strip().lower())
        headers, details = parsed_tuple
        class_script(headers=headers, details=details, search=search_string).generate_script()
    if default:
        # TODO: Generates the default Curl command.
        pass


def generate_script(script, headers, details, search_string=None):
    """Returns the script code for the HTTP request passed in script language

    :param str script: Name of the language for which script is to be generated
    :param dict headers: Headers information
    :param dict details: Details information
    :param str search_string: string to be searched for in the response for given request

    :return: A combined string of generated code
    :rtype: `str`
    """
    class_script = hardcoded_script_import(script.strip().lower())
    return class_script(headers=headers, details=details, search=search_string).generate_script()
