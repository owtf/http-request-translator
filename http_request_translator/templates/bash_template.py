code_begin = """#!/usr/bin/env bash
curl"""


code_header = """ --header "{header}:{value}" """


code_proxy = " -x {proxy}"


code_post = """ --data "{data}" """


code_search = """ | egrep --color " {search_string} |$" """


code_nosearch = """ -v --request {method} {url} {headers} --include"""
