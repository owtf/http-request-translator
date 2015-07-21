from __future__ import print_function

import re


def generate_script(header_dict, details_dict, searchString=None):
    # TODO: Docstring and comments.
    method = details_dict['method'].strip()
    host = details_dict['Host'].strip()
    headers = str(header_dict)
    stripCurlyBrackets = re.sub(r"{|}", "", headers)
    stripUnwantedSingleQuotes = re.sub(r"': '", " : ", stripCurlyBrackets)
    addHeaders = re.sub(r"', '", "\" --header \"", stripUnwantedSingleQuotes)
    addLeadingDoubleQuote = re.sub(r"\'", "\"", addHeaders)
    stripHost = re.sub(r'\"Host\s?[^A-Z]*(?=\")', "", addLeadingDoubleQuote)
    formattedHeaders = re.sub(r"\"", "", stripHost, 1)
    if searchString:
        try:
            if 'proxy' not in details_dict:
                    skeleton_code = '''\
#!/usr/bin/env bash
curl -s --request ''' + method + ''' ''' + host + ''' "''' + formattedHeaders + ''' --include | egrep --color ''' + "'" + searchString + '''|$'
                '''
            else:
                skeleton_code = '''\
#!/usr/bin/env bash
curl -x ''' + details_dict['proxy'] + ''' -s --request ''' + method + ''' ''' + host + ''' "''' + formattedHeaders + ''' --include | egrep --color ''' + "'" + searchString + '''|$'
                '''
        except IndexError:
            print("You haven't given the port Number")
        else:
            return skeleton_code
    else:
        try:
            if 'proxy' not in details_dict:
                skeleton_code = '''\
#!/usr/bin/env bash
curl -s --request ''' + method + ''' ''' + host + ''' "''' + formattedHeaders + ''' --include
                '''
            else:
                skeleton_code = '''\
#!/usr/bin/env bash
curl -x '''+details_dict['proxy']+''' -s --request ''' + method + ''' ''' + host + ''' "''' + formattedHeaders + ''' --include
                '''
        except IndexError:
            print("You haven't given the port Number")
        else:
            return skeleton_code
