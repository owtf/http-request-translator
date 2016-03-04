code_begin = """require "typhoeus"

url = '{url}'

options = {{
    followlocation: true,
    verbose: true,
    method: :{method},
"""


code_proxy = """
    proxy: '{proxy}',
"""


code_header = """
    "{header}" => "{value}","""


code_headers = """
    headers: {{{headers}
    }},
"""


code_post = """
    body: "{data}"
"""


code_search = """
}}
req = Typhoeus::Request.new(url, options)
req.on_complete do |response|
  if response.success?
    puts 'Response #{{response.code}}:'
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

  elsif response.timed_out?
    puts 'Request Timed Out!'
  elsif response.code == 0
    # Could not get an http response, something's wrong.
    puts response.return_message
  else
    # Received a non-successful http response.
    puts 'HTTP request failed: ' + response.code.to_s
  end
end

req.run
"""


code_nosearch = """
}
req = Typhoeus::Request.new(url, options)
req.on_complete do |response|
  if response.success?
    puts 'Response #{response.code}'
    puts response.body

  elsif response.timed_out?
    puts 'Request Timed Out!'
  elsif response.code == 0
    # Could not get an http response, something's wrong.
    puts response.return_message
  else
    # Received a non-successful http response.
    puts 'HTTP request failed: ' + response.code.to_s
  end
end

req.run
"""
