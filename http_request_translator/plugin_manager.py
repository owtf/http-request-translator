from __future__ import print_function


def plugin_manager(script_list, parsed_tuple, searchString=None):
    # TODO: Docstring and comments.
    default = len(script_list) or False
    for script in script_list:
        string = script.lower() + "_script"
        header_dict, details_dict = parsed_tuple
        try:
            __import__(string, globals={"__name__": __name__}).generate_script(
                header_dict,
                details_dict,
                searchString)
        except ImportError:
            print("The support for generating the required Script is not available at the now.")
    if default:
        # generates the default Curl command
        import default
        pass


def generate_script(script_type, headers, details, searchString=None):
    """Returns the script code for the HTTP request passed in `script_type` language

    :param str script_type: Name of the language for which script is to be generated
    :param dict headers: Headers information
    :param dict details: Details information
    :param str searchString: string to be searched for in the response for given request

    :return: A combined string of generated code
    :rtype:`str`

    .. note::

        script_type cannot be a list, Needed in order to faciliate integration

    """
    script_name = script_type.lower() + "_script"
    try:
        return __import__(script_name, globals={"__name__": __name__}).generate_script(
                headers,
                details,
                searchString)
    except ImportError:
        raise ImportError("The support for generating the required Script is not available at the time now.")
