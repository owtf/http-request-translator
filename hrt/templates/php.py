code_begin = """if (!extension_loaded('curl')) {{
    print 'Curl Extension not found. Exiting';
    exit;
}}
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, '{url}');
// Set so curl_exec returns the result instead of outputting it.
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
// Set verbosity
curl_setopt($ch, CURLOPT_VERBOSE, 1);
$headers = array();
"""


code_header = """
$headers[] = "{header}:{value}";
"""


code_proxy = """
curl_setopt($ch, CURLOPT_PROXY, '{proxy}');
"""


code_post = """
$content = "{data}";
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $content);
"""


code_search = """
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$response = curl_exec($ch);

if (curl_errno($ch)) {{
 print curl_error($ch);
}} else {{
 curl_close($ch);
}}
print $response;
$string = "{search_string}";
// Blindly copied from http://stackoverflow.com/questions/10778318/test-if-a-string-is-regex
// Checks if the passed string is a regex or a simple string
if( preg_match("/^\/.+\/[a-z]*$/i",$string)) {{
    if (preg_match($string, $response, $match)) {{
        print 'Found a match!';
    }}
}}
else {{
    if (strpos($response,$string) !== false) {{
        print 'Found a match!';
    }}
}}
"""


code_nosearch = """
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$response = curl_exec($ch);

if (curl_errno($ch)) {
 print curl_error($ch);
} else {
 curl_close($ch);
}
print $response;
"""
