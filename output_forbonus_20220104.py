
# !/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import datetime
import pymysql
import pandas as pd

from sqlalchemy import create_engine
import pymysql
import pandas as pd




def savedt():
    engine_jsMons = create_engine('mysql+pymysql://root:123456@localhost:3306/JS_Mons')


    sql_sp_f = 'select * from onlyforbonus_20220104  ; '
    df_js_f = pd.read_sql_query(sql_sp_f, engine_jsMons)
    print(df_js_f)
    # df.to_excel(excel_writer='demo.xlsx', sheet_name='sheet_1')
    # excel_writer = 'demo.xlsx', sheet_name = 'sheet_1'
    df_js_f.to_excel("onlyforbonus_20220104.xlsx")




if __name__ == '__main__':
    savedt()

