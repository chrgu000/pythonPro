# -*- coding: utf-8 -*

'''
接口：新插入的数据处理接口
  1、新插入楼宇处理接口
  2、新插入楼宇-企业关系处理接口
'''

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options,parse_command_line
import sys
sys.path.append("../")
from insert_ import insert_new_building_a ,insert_new_conn

define('port', default=8002, help='run on the port', type=int)

class basicHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        '''设置响应头
               '''
        # 所有域可以获取数据
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTIONS')
    def get(self):
        self.write("")
    def resultpost(self,data):
        self.write(str(data))

class buildingHandler(basicHandler):
    def post(self):
        try:
            building_name=self.get_argument("building_name")
            building_info=self.get_argument("building_info")
            print(building_name)
            insert_new_building_a(building_name,building_info)
            self.resultpost("success")
        except Exception as e:
            self.resultpost("failed")


class connHandler(basicHandler):
    def post(self):
        try:
            belong_building=self.get_argument("belong_building")
            company_name=self.get_argument("companyName")
            print(belong_building)
            insert_new_conn(belong_building,company_name)
            self.resultpost("success")
        except Exception as e:
            self.resultpost("failed")


def main():
    parse_command_line()
    app=tornado.web.Application([
                    (r'/insertbuilding',buildingHandler),
                    (r'/insertconn',connHandler),
                 ])
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
   main()
   pass

