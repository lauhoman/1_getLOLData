#encoding=utf-8

import urllib
import urllib2
import json
from bs4 import BeautifulSoup
import dataBaseAction

def getUser(user,server):
    try:
        print '开始获取UserID...'
        user=user.decode("utf-8")
        server=server.decode("utf-8")
        check=dataBaseAction.searchDB("select id from user where name='%s' and server='%s'" % (user,server)).fetchone()
        if check!=None:
            print '找到了该用户...'
            return str(check[0])
        searchUserPage=urllib.urlopen("http://www.laoyuegou.com/enter/search/search.html?type=lol&name=%s" % user.encode('utf-8'))
        selectServerPage=BeautifulSoup(str(searchUserPage.read()),"html.parser")
        result=selectServerPage.find_all(class_="curret")
        for item in result:
            #print "1111"
            soup=BeautifulSoup(str(item))
            link=soup.a
            if str(link)!='None':
                #print "2222"
                link=str(link.attrs['href'])
                final=str(urllib2.urlopen(urllib2.Request(link)).read())

                servername=soup.find(class_="col-gray")
                if str(servername)!='None':
                    #print "3333"
                    servername=servername.string
                    servername=servername.split('-')[1][1:]
                    #print "4444"
                    print "服务器匹配中..."+str(servername)
                    if servername==server:
                        print '找到了该用户...'
                        user_id= str(str(BeautifulSoup(final).find(class_='more').attrs['href']).split('/')[4].split('.')[0])
                        dataBaseAction.editDB("INSERT INTO user (id,name,server) VALUES (%s,'%s','%s')" % (user_id,user,server))
                        return user_id
        print 'Error:找不到该用户!'
        return None
    except Exception,e:
        print "Error:getUser Filed:"
        print e
        return None

def getAllMatch(user_id):
    try:
        print '开始获取该用户所有的比赛数据...'
        matchList=[]
        index=1
        for i in range(1,100):
            print "page#%d" % index
            index+=1
            # if index>5:
            #     break
            loadPage=urllib2.urlopen(("http://app.laoyuegou.com/gameLol/matches/id/%s.html?type=-1&pageNow=%d&ajax=1" % (user_id,i)))
            page=loadPage.read()
            if page=='[]':
                break
            else:
                allMatch=json.loads(page)
                for match in allMatch:
                    matchInfo={}
                    url=str(match['url']).split('%2F')
                    matchInfo['id']=url[len(url)-3]
                    matchInfo['win']=(str(match['win'])=='1')
                    matchInfo['start']=(str(match['start_time']))
                    matchInfo['type']=str(match['game_type'])
                    matchList.append(matchInfo)
        if len(matchList)==0:
            print '找不到任何比赛数据...'
            return None
        else:
            print '获取成功...'
            return matchList
    except Exception,e:
        print "Error: getAllMatch Failed:"
        print e
        return None

def getMatch(user_id,pageIndex):
    try:
        print '开始获取该用户的第%d页比赛数据...' % pageIndex
        matchList=[]
        pageIndex+=1
        # if index>5:
        #     break
        loadPage=urllib2.urlopen(("http://app.laoyuegou.com/gameLol/matches/id/%s.html?type=-1&pageNow=%d&ajax=1" % (user_id,pageIndex)))
        page=loadPage.read()
        if page=='[]':
            return None
        else:
            allMatch=json.loads(page)
            for match in allMatch:
                matchInfo={}
                url=str(match['url']).split('%2F')
                matchInfo['id']=url[len(url)-3]
                matchInfo['win']=(str(match['win'])=='1')
                matchInfo['start']=(str(match['start_time']))
                matchInfo['type']=str(match['game_type'])
                matchList.append(matchInfo)
        if len(matchList)==0:
            print '找不到任何比赛数据...'
            return None
        else:
            print '获取成功...'
            return matchList
    except Exception,e:
        print "Error: getMatch Failed!"
        print e
        return None

#getUserID("Lauhoman".decode('utf-8'),'扭曲丛林'.decode('utf-8'))

