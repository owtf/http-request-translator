begin_code = """
#!/usr/bin/env bash
curl"""


request_header = """ --header '{header}:{header_value}' """


code_search = " | egrep --color ' {search_string} |$'"


code_simple = " -v --request {method} {url} {headers} --include"


proxy_code = " -x {proxy}"


post_code = " --data '{post_body}'"
