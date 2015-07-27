begin_code = """
require 'net/http'
require 'uri'

uri = URI('{host}')"""

get_request = """
req = Net::HTTP::Get.new(uri.request_uri)
"""

post_request = """
req = Net::HTTP::Post.new(uri.request_uri)
req.body = '{body}'
"""

request_header = """
req['{header}'] = '{header_value}'"""

proxy_code = """
proxy_host, proxy_port = '{proxy_host}', '{proxy_port}'
http = Net::HTTP.new(uri.hostname, nil, proxy_host, proxy_port)
"""

# NON PROXY
non_proxy_code = """
http = Net::HTTP.new(uri.hostname, uri.port)
"""
# IF HTTPS
https_code = """
http.use_ssl=true
"""

body_code_search = """
response = http.request(req)
puts 'Response #{{response.code}} #{{response.message}}:'

begin
    require 'colorize'
    lib_available = true
rescue LoadError
    lib_available = false
end

matched = response.body.match /{search_string}/

original = response.body
if matched then
    if lib_available then
        for i in 0..matched.length
            original.gsub! /#{{matched[i]}}/, "#{{matched[i]}}".green
        end
    else
        for i in 0..matched.length
            puts 'Matched item: #{{matched[i]}}'
        end
    end
end
puts original
"""

body_code_simple = """
response = http.request(req)
puts "Response #{response.code} #{response.message}:
          #{response.body}"
"""
