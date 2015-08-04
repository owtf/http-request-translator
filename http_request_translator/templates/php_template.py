begin_code = """
if (!extension_loaded('curl')) {{
    print 'Curl Extension not found. Exiting';
    exit;
}}
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, '{url}');
// Set so curl_exec returns the result instead of outputting it.
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$headers = array();
"""

request_header = """
$headers[] = "{header}:{header_value}";
"""

post_request = """
$content = '{body}';
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $content);
"""

proxy_code = """
curl_setopt($ch, CURLOPT_PROXYPORT, {proxy_port});
curl_setopt($ch, CURLOPT_PROXY, {proxy_host});
"""

req_code = """
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$response = curl_exec($ch);

if (curl_errno($ch)) {
 print curl_error($ch);
} else {
 curl_close($ch);
}
"""
search_code = """
print $response;
$string = '{search_string}';
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

non_search_code = """
print $response;
"""
