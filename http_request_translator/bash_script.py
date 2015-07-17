from __future__ import print_function

import re


def generate_script(header_dict, details_dict, searchString=None):
    # TODO: Docstring and comments.
    method = details_dict['method'].strip()
    headers = str(header_dict)
    a = re.sub(r"{|}", "", headers)
    b = re.sub(r"': '", " : ", a)
    c = re.sub(r"', '", "\" --header \"", b)
    d = re.sub(r"\'", "\"", c)
    e = re.sub(r"\"Host :", "", d)
    formattedHeaders = re.sub(r"\"", "", e, 1)
    if searchString:
        try:
            if 'proxy' not in details_dict:
                    skeleton_code = '''\
#!/usr/bin/env bash
curl -s --request ''' + method + formattedHeaders + ''' --include | egrep --color ''' + "'" + searchString + '''|$'
                '''
            else:
                skeleton_code = '''\
#!/usr/bin/env bash
curl -x ''' + details_dict['proxy'] + ''' -s --request ''' + method + formattedHeaders + ''' --include | egrep --color ''' + "'" + searchString + '''|$'
                '''
        except IndexError:
            print("You haven't given the port Number")
        else:
            print(skeleton_code)
    else:
        try:
            if 'proxy' not in details_dict:
                skeleton_code = '''\
#!/usr/bin/env bash
curl -s --request '''+method+formattedHeaders+''' --include
                '''
            else:
                skeleton_code = '''\
#!/usr/bin/env bash
curl -x '''+details_dict['proxy']+''' -s --request '''+method+formattedHeaders+''' --include
                '''
        except IndexError:
            print("You haven't given the port Number")
        else:
            print(skeleton_code)
