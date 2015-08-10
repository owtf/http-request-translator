from __future__ import print_function


def hardcoded_script_import(script_name):
    """Manually import the generate_script function of the script.

    :param str script_name: Name of the script from which to import the function.

    :raises ValueError: When the script is not supported.

    :return: The generate_script function of the `script_name` script.
    :rtype: function
    """
    if script_name == 'bash':
        from .bash_script import generate_script as gs
    elif script_name == 'php':
        from .php_script import generate_script as gs
    elif script_name == 'python':
        from .python_script import generate_script as gs
    elif script_name == 'ruby':
        from .ruby_script import generate_script as gs
    else:
        raise ValueError("The '%s' language is not supported yet." % script_name)
    return gs


def plugin_manager(script_list, parsed_tuple, search_string=None):
    # TODO: Docstring and comments.
    default = len(script_list) or False
    for script in script_list:
        generate_script = hardcoded_script_import(script.strip().lower())
        header_dict, details_dict = parsed_tuple
        generate_script(header_dict, details_dict, search_string)
    if default:
        # TODO: Generates the default Curl command.
        pass


def generate_script(script, headers, details, search_string=None):
    """Returns the script code for the HTTP request passed in `script` language

    :param str script: Name of the language for which script is to be generated
    :param dict headers: Headers information
    :param dict details: Details information
    :param str search_string: string to be searched for in the response for given request

    :return: A combined string of generated code
    :rtype:`str`
    """
    generate_script = hardcoded_script_import(script.strip().lower())
    return generate_script(headers, details, search_string)
