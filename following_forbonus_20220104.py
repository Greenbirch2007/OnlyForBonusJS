


import datetime
import time

import pymysql
import requests
from lxml import etree
import json
from queue import Queue
import threading
from requests.exceptions import RequestException




from retrying import retry

def retry_if_io_error(exception):
    return isinstance(exception, ZeroDivisionError)






'''
1. 创建 URL队列, 响应队列, 数据队列 在init方法中
2. 在生成URL列表中方法中,把URL添加URL队列中
3. 在请求页面的方法中,从URL队列中取出URL执行,把获取到的响应数据添加响应队列中
4. 在处理数据的方法中,从响应队列中取出页面内容进行解析, 把解析结果存储数据队列中
5. 在保存数据的方法中, 从数据队列中取出数据,进行保存
6. 开启几个线程来执行上面的方法
'''

def run_forever(func):
    def wrapper(obj):
        while True:
            func(obj)
    return wrapper


def RemoveDot(item):
    f_l = []
    for it in item:

        f_str = "".join(it.split(","))
        ff_str = f_str +"00"
        f_l.append(ff_str)

    return f_l

def remove_douhao(num):
    num1 = "".join(num.split(","))
    f_num = str(num1)
    return f_num
def remove_block(items):
    new_items = []
    for it in items:
        f = "".join(it.split())
        new_items.append(f)
    return new_items
def call_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


class JSPool_M(object):

    def __init__(self,url):
        self.url = url

    def page_request(self):
        ''' 发送请求获取数据 '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }

        response = requests.get(self.url,headers=headers)
        if response.status_code == 200:
            html = response.text
            return html
        else:
            pass

    def page_parse_(self):
        '''根据页面内容使用lxml解析数据, 获取段子列表'''


        html  = self.page_request()
        element = etree.HTML(html)

        now_price = element.xpath(
            '//*[@id="layout"]/div[2]/div[3]/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[2]/div/text()')
        f_price = RemoveDot(remove_block(now_price))
        big_list.append(float(f_price[0]))
        return big_list




def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JS_Mons',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    try:
        f_ls = "%s," * 26# 这里错了
        fc = "J225,J400,J9101, J9104, J2914, J6178, J4502, J9434, J1820, J9810, J8316, J9506, J4902, J9504, J1720, J8411, J9513, J9508, J8308, J8304, J5020, J1808, J8892, J9503, J7167, J8593"
        print(fc)
        print(f_ls[:-1])
        cursor.executemany('insert into onlyforbonus_20220104 ({0}) values ({1})'.format(fc,f_ls[:-1]), content)
        connection.commit()
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass





def get_index():
    index_code = ["0000", "0040"]
    for i_code in index_code:
        url ='https://kabutan.jp/stock/?code={0}'.format(i_code)
        html =call_page(url)
        element = etree.HTML(html)

        now_price = element.xpath('//*[@id="stockinfo_i1"]/div[2]/span[2]/text()')
        f_price = RemoveDot(remove_block(now_price))
        big_list.append(float(f_price[0]))




if __name__ == '__main__':
    big_list = []
    get_index()
    js225_400_codes = ["9101","9104","2914","6178","4502","9434","1820","9810","8316","9506","4902","9504","1720","8411","9513","9508","8308","8304","5020","1808","8892","9503","7167","8593"]



    for it in js225_400_codes:
        url = 'https://minkabu.jp/stock/{0}'.format(it)
        print(url)
        jsp = JSPool_M(url)# 这里把请求和解析都进行了处理
        jsp.page_parse_()
    ff_l = []
    f_tup = tuple(big_list)
    ff_l.append((f_tup))
    print(ff_l)
    print(big_list)
    insertDB(ff_l)























 #   create table onlyforbonus_20220104 (id int not null primary key auto_increment,J225 float,J400 float,J9101 FLOAT, J9104 FLOAT, J2914 FLOAT, J6178 FLOAT, J4502 FLOAT, J9434 FLOAT, J1820 FLOAT, J9810 FLOAT, J8316 FLOAT, J9506 FLOAT, J4902 FLOAT, J9504 FLOAT, J1720 FLOAT, J8411 FLOAT, J9513 FLOAT, J9508 FLOAT, J8308 FLOAT, J8304 FLOAT, J5020 FLOAT, J1808 FLOAT, J8892 FLOAT, J9503 FLOAT, J7167 FLOAT, J8593 FLOAT,LastTime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ) engine=InnoDB  charset=utf8;


