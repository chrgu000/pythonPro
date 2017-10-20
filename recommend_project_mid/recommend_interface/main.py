# -*- coding: utf-8 -*

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options,parse_command_line

import sys
sys.path.append("../")
from get_ import get_recommend_result

define('port', default=8000, help='run on the port', type=int)

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
    def requestPost(self,data,returnCode=1):
        ret = {"returnCode": returnCode, "data": data}
        self.write(str(ret))

class recommendHandler(basicHandler):
    def post(self):
        company_code = self.get_argument("companyCode")
        try:
            print(company_code)
            # 将每天调用推荐的company记录，用于定时任务中更新模型

            file = open("../model/cur_company.txt", 'a')
            file.write(company_code)
            file.write('\n')
            file.close()
            has_cache = os.path.exists("../recommend_cache/" + company_code +".txt")
            result_list = []
            if has_cache is False:
                result_list = get_recommend_result(company_code)
            else:
                file = open("../recommend_cache/" + company_code +".txt")
                read_file = file.readlines()
                for i in range(0, len(read_file)):
                    result_list.append(read_file[i].replace("\n", ""))
                os.remove("../recommend_cache/" + company_code +".txt")

            if type(result_list) != str:
                self.requestPost(result_list)
            else:
                self.requestPost("error!")
        except Exception as e:
            infostr = -1
            self.requestPost(infostr)

class cacheHandler(basicHandler):
    def post(self):
        company_code = self.get_argument("companyCode")
        result_list = get_recommend_result(company_code)
        file = open("../recommend_cache/" + company_code +".txt", 'a')
        for i in range(0, len(result_list)):
            file.write(result_list[i][0]+","+result_list[i][1])
            file.write('\n')
        file.close()


def main():
    parse_command_line()
    app = tornado.web.Application([(r'/recommend', recommendHandler), (r'/recommend/cache', cacheHandler),])
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
   main()
   pass
