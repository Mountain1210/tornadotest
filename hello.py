# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import base64
import requests
import json
import datetime
import time
import urlparse
import sys, urllib
import os.path




from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)



# client_key = '<YOUR-KEY-HERE>'
# client_secret = '<YOUR-SECRET-HERE>'
# key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
# b64_encoded_key = base64.b64encode(key_secret)
# b64_encoded_key = b64_encoded_key.decode('ascii')
# base_url = 'https://api.twitter.com/'
# auth_url = '{}oauth2/token'.format(base_url)
# print(auth_url)
# auth_headers = {'Authorization': 'Basic {}'.format(b64_encoded_key),
#                 'Content-Type':
#                 'application/x-www-form-urlencoded;charset=UTF-8'
#                 }


# auth_data = {'grant_type': 'client_credentials'}
# # auth_resp = requests.post(auth_url, headers=auth_headers,data=auth_data)
# auth_resp = requests.post(auth_url,data=auth_data)
# # print(auth_resp.json())
# # access_token = auth_resp.json()['access_token']
# # search_headers = {'Authorization': 'Bearer {}'.format(access_token)}
# search_headers = {'Authorization': 'ddddddddd'}
# search_url = '{}1.1/search/tweets.json?'.format(base_url)


class DefaultHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        """对应http的get请求方式"""
        self.write(greeting + ', friendly user!')

    def write_error(self, status_code, **kwargs):
        self.write("Gosh darnit, user! You caused a %d error." % status_code)

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

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2, made=verb,
                difference=noun3)
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "in.html",
            page_title="测试账号",
            header_text = "Header goes here",
            footer_text = "Footer goes here"
        )

class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('hello.html')

class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'

class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('modules/book.html', book=book)

    def embedded_javascript(self):
        return "document.write(\"<p>embedded_javascript()</p>\")"

    def embedded_css(self):
        return ".addition {color: #A1CAF1}"

    def javascript_files(self):
        return "/static/js/a.js"



class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "recommended.html",
            page_title="Burt's Books | Recommended Reading",
            header_text="Recommended Reading",
            footer_text = "Footer goes here",
            books=[{
                    "title":"Programming Collective Intelligence",
                    "subtitle": "Building Smart Web 2.0 Applications",
                    "image":"/static/images/collective_intelligence.gif",
                    "author": "Toby Segaran",
                    "date_added":1310248056,
                    "date_released": "August 2007",
                    "isbn":"978-0-596-52932-1",
                    "description":"<p>This fascinating book demonstrates how you "
                        "can build web applications to mine the enormous amount of data created by people "
                        "on the Internet. With the sophisticated algorithms in this book, you can write "
                        "smart programs to access interesting datasets from other web sites, collect data "
                        "from users of your own applications, and analyze and understand the data once "
                        "you've found it.</p>"
                }
            ]
        )

class SyncHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument('q')
        print('==========')
        print(query)
        search_params = {'q': query, 'result_type': 'recent',
                         'count': 100}

        client = tornado.httpclient.HTTPClient()
        # response = client.fetch(search_url +
        #                         urllib.urlencode(search_params),
        #                         headers=search_headers)
        # body = json.loads(response.body)
        # result_count = len(body['statuses'])
        # now = datetime.datetime.utcnow()
        # raw_oldest_tweet_at = body['statuses'][-1]['created_at']
        # oldest_tweet_at = \
        #     datetime.datetime.strptime(
        #         raw_oldest_tweet_at,
        #         '%a %b %d %H:%M:%S +0000 %Y'
        #         )
        # seconds_diff = time.mktime(now.timetuple()) \
        #     - time.mktime(oldest_tweet_at.timetuple())
        # tweets_per_second = float(result_count) / seconds_diff
        self.write("""
        <div style="text-align: center">
        <div style="font-size: 72px">%s</div>
        <div style="font-size: 144px">%.02f</div>
        <div style="font-size: 24px">tweets per second</div>
        </div>""" % (3000, 400))

class CookHandler(tornado.web.RequestHandler):
    def get(self):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1
        # self.set_cookie('cookie_test1','xiaobai') #默认过期时间是浏览器关闭会话时
        # self.set_cookie('cookie_test2','xiaobai',expires=time.time() + 60) #设置过期时间为60秒
        # self.set_cookie('cookie_test3','xiaobai',expires_days=1) #设置过期时间1天
        # self.set_cookie('cookie_test4','xiaobai',path='/test') #设置路径,限定哪些内容需要发送cookie,/表示全部
        # self.set_cookie('cookie_test5','xiaobai',httponly=True) #设置js不能获取cookie
        # self.set_cookie('cookie_test6','xiaobai',max_age=120,expires=time.time()+60) ##max_age优先级比expires高，前面为120s，所以根据前面的来
        # self.set_secure_cookie('cookie_test7','jiami') #设置一个加密的cookie,但是必须在下面的application里面添加cookie_secret = 'test'，才可以
        countString = "1 time" if count == 1 else "%d times" % count

        self.set_secure_cookie("count", str(count),expires=time.time() + 60)

        self.write(
            '<html><head><title>Cookie Counter</title></head>'
            '<body><h1>You’ve viewed this page %s times.</h1>' % countString + 
            '</body></html>'
        )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": True
    }
    app = tornado.web.Application(
        handlers=[
            (r"/default", DefaultHandler),
            (r"/index", IndexHandler),
            (r"/reverse/(\w+)", ReverseHandler),
            (r"/widget/(\d+)", WidgetHandler2),
            (r"/wrap", WrapHandler),
            (r"/poem", PoemPageHandler),
            (r"/in", MainHandler),
            (r"/hello", HelloHandler),
            (r"/rd", RecommendedHandler),
            (r"/sync", SyncHandler),
            (r"/cook", CookHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        ui_modules=[{'Book': BookModule},{'Hello': HelloModule}],
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()