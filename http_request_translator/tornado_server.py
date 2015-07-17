import tornado.httpserver
import tornado.ioloop
import tornado.httputil as hutil

def handle_request(request):

	message = request.headers
	request.connection.write_headers(
		tornado.httputil.ResponseStartLine('HTTP/1.1', 200, 'OK'),
		tornado.httputil.HTTPHeaders
		({"Content-Length": str(len(str(message)))}))

	request.connection.write(str(message))
	request.connection.finish()
	print(request.headers)

http_server = tornado.httpserver.HTTPServer(handle_request)
http_server.listen(8888, address='127.0.0.1')
tornado.ioloop.IOLoop.instance().start()