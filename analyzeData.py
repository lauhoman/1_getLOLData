import sqlite3
import dataBaseAction


def moneyPerMin(name,server,match=''):

    if match!='':
        sql="select money,time from matchDetail,matchInfo where matchInfo.match_id=matchDetail.match_id and name='%s'and server='%s' and matchDetail.match_id=%s" % (name,server,match)
    else:
        sql="select money,time from matchDetail,matchInfo where matchInfo.match_id=matchDetail.match_id and  name='%s'and server='%s'" % (name,server)
    money=0.0
    time=0.0
    for row in dataBaseAction.searchDB(sql):
        money+=float(row[0])
        time+=float(row[1][0:2])
    return money/time*1000

def pusheyePerMoney(name,server,match=''):
    if match!='':
        sql="select money,pusheye from matchDetail,matchInfo where matchInfo.match_id=matchDetail.match_id and name='%s'and server='%s' and matchDetail.match_id=%s" % (name,server,match)
    else:
        sql="select money,pusheye from matchDetail,matchInfo where matchInfo.match_id=matchDetail.match_id and  name='%s'and server='%s'" % (name,server)
    money=0.0
    pusheye=0.0
    for row in dataBaseAction.searchDB(sql):
        money+=float(row[0])
        pusheye+=float(row[1])
    return pusheye*75/(money*1000)

def damagePerMoney(name,server,match=''):
    if match!='':
        sql="select money,damage from matchDetail,matchInfo where matchInfo.match_id=matchDetail.match_id and name='%s'and server='%s' and matchDetail.match_id=%s" % (name,server,match)
    else:
        sql="select money,damage from matchDetail,matchInfo where matchInfo.match_id=matchDetail.match_id and  name='%s'and server='%s'" % (name,server)
    money=0.0
    damage=0.0
    for row in dataBaseAction.searchDB(sql):
        money+=float(row[0])
        damage+=float(row[1])
    return damage/(money*1000)