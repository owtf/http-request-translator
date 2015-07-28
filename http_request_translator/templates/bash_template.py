begin_code = """
#!/usr/bin/env bash
curl -s --request """

request_header = """ --header "{header} : {header_value}" """

code_search = " | egrep --color ' {search_string} |$' "

code_simple = "{method} {url} {headers} --include "

proxy_code = "-x {proxy}"

body_code = " --data '{body}' "
