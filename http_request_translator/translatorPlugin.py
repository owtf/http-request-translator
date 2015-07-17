from __future__ import print_function


def pluginManager(script_list, parsed_tuple, searchString=None):
    # TODO: Docstring and comments.
    default = len(script_list) or False
    for script in script_list:
        string = script.lower() + "Scripts"
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
