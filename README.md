A HTTP request translator, a *standalone* *tool* that can:

1) Be used from inside OR outside of OWTF.

2) Translate raw HTTP requests into curl commands or bash/python/php/ruby/PowerShell scripts

3) Provide essential quick and dirty transforms: base64 (encode/decode), urlencode (encode/decode)

Quick Tip:
The translator.py when executed with "--help" option will give the manual page of tool.

How to use the tool: 
1) Translating raw request from the CLI to a single script(say python):
	
	$python translator.py --output python --Request "<Your Request>"

2) Translating raw request from the CLI to multiple scripts(say python and bash)

	$python translator.py --output python,bash --Request "<Your Request>"

3) Translating raw request from the CLI by passing data along the request
	
	$python translator.py --output <your favorite script(s)> --data "<body/url parameters to be sent>" --Request "Your Request"

4) Translating raw request to a script that uses a proxy server for sending request
	
	$python translator.py --output <your favorite script(s)> --data "<body/url parameters to be sent>" --proxy "<proxy server that you want to use>" --Request "Your Request"

	If you haven't specified the proxy server, it will use OWTF's defauly inbound proxy

5) Search the response header using the regex-search or the normal string search 
	
	$python translator.py --stringSearch "<String that you want to search in response>" --Request "Your Request"

	For regex search :
	$python translator.py --regexSearch "<String that you want to search in response>" --Request "Your Request"

6) Translating a bunch of raw requests from CLI using the -i option. 

	$python translator.py --output <your favorite script> -i

	Hit enter twice after entering the request and the body(Also the URL parameters for GET requests). Keep translating as much as you want! To come out of the interactive mode, type "q!".

7) To write the output of transformed request to a file 

	$python translator.py --output <your favorite script(s)> --data "<body/url parameters to be sent>" --proxy "<proxy server that you want to use>" --Request "<Your Request>" > <filename.<extension>>

8) Read request from a file and transform it 

	$ python translator.py --output <your favorite script(s)> --Request "`cat <path/to/directory/file_name>`"
