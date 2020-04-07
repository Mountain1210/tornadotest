# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import url, RequestHandler
import json

define("port", default=8000, type=int, help="run server on the given port.")

class IndexHandler(RequestHandler):
    

    def prepare(self):
        if self.request.headers.get("Content-Type").startswith("application/json"):
            self.json_dict = json.loads(self.request.body)
            print self.json_dict
        else:
            self.json_dict = None

    def get(self):
        python_url = self.reverse_url("python_url")
        print python_url
        self.write('<a href="%s"><h1>itcast</h1></a>' %
                   python_url)

    def post(self):
        if self.json_dict:
            for key, value in self.json_dict.items():
                self.write("<h3>%s</h3><p>%s</p>" % (key, value))

    def put(self):
        if self.json_dict:
            for key, value in self.json_dict.items():
                self.write("<h3>%s</h3><p>%s</p>" % (key, value))

class ItcastHandler(RequestHandler):
    def initialize(self, subject):
        self.subject = subject

    def get(self):
        self.write(self.subject)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
            (r"/", IndexHandler),
            (r"/cpp", ItcastHandler, {"subject":"c++"}),
            url(r"/python1123", ItcastHandler, {"subject":"python"}, name="python_url")
        ],
        debug = True)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()