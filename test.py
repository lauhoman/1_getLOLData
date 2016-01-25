# -*- coding: UTF-8 -*-
import urllib2
import json
import getID
import sys
import sqlite3
from bs4 import BeautifulSoup
import getData
import dataBaseAction
import analyzeData
reload(sys)
sys.setdefaultencoding( "utf-8" )


l=('半梦半醒半浮生oc','叶少阳','阵雨淋天','Royal护卫队灬')
# for item in l:
#     print item
#     getData.getData(item,'扭曲丛林')

for item in l:
    print item
    print analyzeData.pusheyePerMoney(item,'扭曲丛林')
# getData.getData('SoCaibility','扭曲丛林')

#print dataBaseAction.searchDB("select * from matchDetail where name='安分守己9'").fetchone()[0]


# print analyzeData.damagePerMoney('SoCreepy','扭曲丛林','868580140')
#print analyzeData.pusheyePerMoney('半梦半醒','扭曲丛林')