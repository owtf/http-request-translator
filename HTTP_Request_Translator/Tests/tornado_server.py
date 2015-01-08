import tornado.httpserver
import tornado.ioloop

def handle_request(request):
	request.connection.write_headers(
		httputil.ResponseStartLine('HTTP/1.1', 200, 'OK'),
		{"Content-Length": str(len(message))})
	request.connection.write(request)
	request.connection.finish()

http_server = tornado.httpserver.HTTPServer(handle_request)
http_server.listen(8888)
tornado.ioloop.IOLoop.instance().start()