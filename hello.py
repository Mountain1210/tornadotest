# coding:utf-8

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
    	greeting = self.get_argument('greeting', 'Hello')
        """对应http的get请求方式"""
        self.write(greeting + ', friendly user!')

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))

class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])

# matched with (r"/widget/(\d+)", WidgetHandler2)
class WidgetHandler2(tornado.web.RequestHandler):
    def get(self,widget_id):
        # widget = retrieve_from_db(widget_id)
        self.write(widget_id)

    def post(self, widget_id):
        widget = retrieve_from_db(widget_id)
        widget['foo'] = self.get_argument('foo')
        save_to_db(widget)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
		handlers=[
			(r"/default", IndexHandler),
			(r"/reverse/(\w+)", ReverseHandler),
			(r"/widget/(\d+)", WidgetHandler2),
			(r"/wrap", WrapHandler)
		]
	)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()