#encoding:utf-8
import sys
import getID
import urllib2
import time
import sqlite3
from bs4 import BeautifulSoup
import dataBaseAction

def getData(name,server):
    #try:
        print "开始数据收集..."
        user_id=getID.getUser(name,server)
        if user_id!=None:
            allMatch=getID.getAllMatch(user_id)
        else:
            return None
        index=0
        for each in allMatch:
            try:
                index+=1
                print "match#"+str(index)

                check=dataBaseAction.searchDB("select * from matchInfo where match_id=%s" % each['id']).fetchone()!=None
                if check:
                    print "本场比赛已经读取过了..."
                    continue


                detailPage=urllib2.urlopen("http://app.laoyuegou.com/gameLol/matchDetail/matchId/%s/id/%s.html" % (each['id'],user_id))
                detail=detailPage.read()
                soup=BeautifulSoup(detail,"html.parser")

                match_id=each['id']
                date=each['start']
                time=soup.find_all(class_='time')
                begin=time[0].string
                time=time[1].string
                game_type=each['type']
                blue=soup.find_all(class_='record-details-box')
                red=blue[1]
                blue=blue[0]
                player_index=0
                sql=[]
                win=[]
                player_name=[]
                kill=[]
                death=[]
                ass=[]
                side=['blue', 'blue', 'blue', 'blue', 'blue', 'red', 'red', 'red', 'red', 'red']
                skill_1=[]
                skill_2=[]
                w=[[],[],[],[],[],[],[]]
                eye=[]
                hero=[]
                damage=[]
                undergo=[]
                money=[]
                lasthit=[]
                pusheye=[]
                pulleye=[]




                sql.append(('''INSERT INTO matchInfo (match_id,date,begin,time,server,type) VALUES (%s,'%s','%s','%s','%s','%s')''') % (match_id,date,begin,time,server,game_type))

                for item in blue.find_all('h6')[1:]:
                    player_name.append(item.string)
                for item in red.find_all('h6')[1:]:
                    player_name.append(item.string)

                for item in blue.find_all(class_='cord-time'):
                    kda=item.string.split('/')
                    kill.append(kda[0])
                    death.append(kda[1])
                    ass.append(kda[2])
                for item in red.find_all(class_='cord-time'):
                    kda=item.string.split('/')
                    kill.append(kda[0])
                    death.append(kda[1])
                    ass.append(kda[2])

                temp=1
                for item in blue.find_all(class_='skill-img'):
                    if temp==1:
                        skill_1.append(str(item.attrs['src'])[48:].split('.')[0])
                        temp=2
                    else:
                        skill_2.append(str(item.attrs['src'])[48:].split('.')[0])
                        temp=1
                temp=1
                for item in red.find_all(class_='skill-img'):
                    if temp==1:
                        skill_1.append(str(item.attrs['src'])[48:].split('.')[0])
                        temp=2
                    else:
                        skill_2.append(str(item.attrs['src'])[48:].split('.')[0])
                        temp=1

                temp=0
                for item in blue.find_all(class_='photo-img'):
                    img=str(item.attrs['src'])[110:].split('.')[0]
                    if temp==6:
                        eye.append(img)
                        temp=-1
                    else:
                        w[temp].append(img)
                    temp+=1

                temp=0
                for item in red.find_all(class_='photo-img'):
                    img=str(item.attrs['src'])[110:].split('.')[0]
                    if temp==6:
                        eye.append(img)
                        temp=-1
                    else:
                        w[temp].append(img)
                    temp+=1

                for item in blue.find_all(class_='record-img'):
                    img=str(item.attrs['src']).split('%2F')[-1].split('.')[0]
                    hero.append(img)
                for item in red.find_all(class_='record-img'):
                    img=str(item.attrs['src']).split('%2F')[-1].split('.')[0]
                    hero.append(img)

                temp=0
                for item in blue.find_all('script'):
                    temp+=1
                    sum=str(item.string).split('\n')[7].split(' ')[-1][1:]
                    sum=sum[0:len(sum)-2]
                    if temp==1:
                        sum=sum.replace(',','')
                        damage.append(sum)
                    elif temp==2:
                        sum=sum.replace(',','')
                        undergo.append(sum)
                    elif temp==3:
                        sum=sum.replace('K','')
                        money.append(sum)
                    elif temp==4:
                        sum=sum.replace(',','')
                        lasthit.append(sum)
                        temp=0
                temp=0
                for item in red.find_all('script'):
                    temp+=1
                    sum=str(item.string).split('\n')[7].split(' ')[-1][1:]
                    sum=sum[0:len(sum)-2]
                    if temp==1:
                        sum=sum.replace(',','')
                        damage.append(sum)
                    elif temp==2:
                        sum=sum.replace(',','')
                        undergo.append(sum)
                    elif temp==3:
                        sum=sum.replace('K','')
                        money.append(sum)
                    elif temp==4:
                        sum=sum.replace(',','')
                        lasthit.append(sum)
                        temp=0
                temp=1
                for item in blue.find_all(class_='negative-plan'):
                    for item2 in item.find_all('i'):
                        if temp==1:
                            pusheye.append(item2.string)
                            temp=2
                        else:
                            pulleye.append(item2.string)
                            temp=1
                temp=1
                for item in red.find_all(class_='negative-plan'):
                    for item2 in item.find_all('i'):
                        if temp==1:
                            pusheye.append(item2.string)
                            temp=2
                        else:
                            pulleye.append(item2.string)
                            temp=1

                for temp in range(0,10):
                    if player_name[temp]==name:
                        if temp>=5:
                            if each['win']==True:
                                win=['0','0','0','0','0','1','1','1','1','1']
                            else:
                                win=['1','1','1','1','1','0','0','0','0','0']
                        else:
                            if each['win']==True:
                                win=['1','1','1','1','1','0','0','0','0','0']
                            else:
                                win=['0','0','0','0','0','1','1','1','1','1']
                # print len(player_name)
                # print len(side)
                # print len(win)
                # print len(kill)
                # print len(death)
                # print len(ass)
                # print len(skill_1)
                # print len(skill_2)
                # print len(w[0])
                # print len(w[1])
                # print len(w[2])
                # print len(w[3])
                # print len(w[4])
                # print len(w[5])
                # print len(eye)
                # print len(hero)
                # print len(damage)
                # print len(undergo)
                # print len(money)
                # print len(lasthit)
                # print len(pusheye)
                # print len(pulleye)
                #
                # print hero
                # hero=hero[1:]
                # for item in w:
                #     print item
                for temp in range(0,10):
                    # print 'temp='+str(temp)
                    sen='''INSERT INTO matchDetail (match_id,name,side,win,kill,death,ass,skill_1,skill_2,w1,w2,w3,w4,w5,w6,eye,hero,damage,undergo,money,lasthit,pusheye,pulleye) VALUES (%s,'%s','%s',%s,%s,%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s)''' % (match_id,player_name[temp],side[temp],win[temp],kill[temp],death[temp],ass[temp],skill_1[temp],skill_2[temp],w[0][temp],w[1][temp],w[2][temp],w[3][temp],w[4][temp],w[5][temp],eye[temp],hero[temp],damage[temp],undergo[temp],money[temp],lasthit[temp],pusheye[temp],pulleye[temp])
                    sql.append(sen)
                    #print sql

                dataBaseAction.editDB(sql)
            except Exception,e:
                print 'Failed to get Data!'

    # except Exception,e:
    #     print 'Error: getDataFailed:'
    #     print e

#getData('Lauhoman','扭曲丛林')