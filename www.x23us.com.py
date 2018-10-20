# encoding: utf-8
import requests
import re
import MySQLdb
import time

conn = MySQLdb.Connect(host='139.199.157.103',
                       port=3306,
                       user='zuoye2',
                       passwd='zhangjun',
                       db='zuoye2',
                       charset='utf8'
                       )
cursor = conn.cursor()
print "数据库连接成功！"

sqlxid = "select x_id from x_xiaoshuo order by x_id desc LIMIT 1"
cursor.execute(sqlxid)
sx_id = cursor.fetchone()[0]
print "sql select chenggong"


# 小说ID
x_id = sx_id+1
print "xid=", x_id
# 小说字数
zishu = 67731
# 连接符
lj = "_"

asdy = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Host':'zhannei.baidu.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

xsurl = 'https://www.x23us.com/html/70/70985/'


def sqlmulu(zjtitles,zjid):
    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sqlmulu = "INSERT INTO x_mulu(x_ids, x_zjid, x_zjnr, times) " \
          "VALUES(%s, '%s', '%s', '%s')" % (x_id, zjid, zjtitles, times)
    cursor.execute(sqlmulu)
    print zjid, zjtitle, "写入成功！", times

def sqlneirong(zjid, qx, jss):
    sqlneirong = "insert into x_neirong(x_neirong, x_zjids, ids, x_ids) values ('%s', '%s', %s, '%s')" % (zjid, qx, jss, x_id)
    cursor.execute(sqlneirong)
    print "章节写入成功！"

def sqlxiaoshuoxinxi(x_name,x_zuozhe,x_tupian, x_jianjie):
    sql = "INSERT INTO x_xiaoshuo(x_id, x_name, jianjie, x_fengmian, zuozhe, zishu) VALUES(%s, '%s', '%s', '%s', '%s', %s)" % (x_id, x_name, x_jianjie, x_tupian, x_zuozhe, zishu)
    cursor.execute(sql)
    print "小说信息获取并写入数据库成功！"

def gatxszhangjie(zjurl,zjtitle,js):
    zjtitles = zjtitle
    dakai2 = requests.get(xsurl+zjurl)
    dakai2.encoding = "gbk"
    jieguo2 = dakai2.text
    pp2 = r'<dd id="contents">(.*?)</dd>'
    title2 = re.findall(pp2, jieguo2, re.S)[0]
    qx = re.sub("<br />", "\n", title2)
    zjid = "%d%s%d" % (x_id, lj, js)
    jss = js
    sqlmulu(zjtitles, zjid)
    sqlneirong(qx, zjid, jss)
    #
    # print qx, zjid
    # print qx, zjid, zjtitles,  jss

js = 1
dakai = requests.get(xsurl)
dakai.encoding = "gbk"
jieguo = dakai.text
# 小说信息匹配-小说名字
pp2 = r'<meta name="og:novel:book_name" content="(.*?)"/> '
x_name = re.findall(pp2, jieguo)[0]
x_name.encode(encoding='UTF-8')

# 小说信息匹配-小说作者
pp2 = r'<meta name="og:novel:author" content="(.*?)"/> '
x_zuozhe = re.findall(pp2, jieguo)[0]
x_zuozhe.encode(encoding='UTF-8')

# 小说信息匹配-小说封面
pp2 = r'<meta property="og:image" content="(.*?)"/> '
x_tupian = re.findall(pp2, jieguo)[0]
x_tupian.encode(encoding='UTF-8')

# 小说信息匹配-小说简介
pp2 = r'<meta property="og:description" content="(.*?)"/> '
x_jianjie = re.findall(pp2, jieguo, re.S)[0]
x_jianjie.encode(encoding='UTF-8')

# 提交小说信息保存数据库
sqlxiaoshuoxinxi(x_name, x_zuozhe, x_tupian, x_jianjie)
print x_name, x_zuozhe, x_tupian, x_jianjie

# # 匹配选取
pp2 = r'<dd><table cellspacing="1" cellpadding="0" bgcolor="#E4E4E4" id="at">.*?</table>'
x_name = re.findall(pp2, jieguo, re.S)[0]

pp = r'<a href="(.*?)">(.*?)</a>'
title = re.findall(pp, x_name)
for zjurl,zjtitle in title:
    gatxszhangjie(zjurl, zjtitle, js)
    # print zjurl, zjtitle, js
    js = js + 1


print "小说爬取完毕"

conn.close()
cursor.close()
print "已断开数据库连接！"

