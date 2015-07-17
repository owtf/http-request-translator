#!/usr/bin/python

def pluginManager(script_list, parsed_tuple, searchString=None):

	default = True
	if not len(script_list) == 0 :
		default = False

	for x in range(0, len(script_list)) :
		string = script_list[x].lower() + "Scripts"

        try:
            __import__(string, globals={"__name__": __name__}).generate_script(parsed_tuple[0],
                                                                               parsed_tuple[1], searchString)

		except ImportError :
			print("The support for generating the\
			required Script is not available at the now,\
			 might be added in the future :) ")

	if default :
		#generates the default Curl command
		import default
		pass

