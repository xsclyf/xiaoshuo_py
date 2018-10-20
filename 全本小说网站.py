# encoding: utf-8
import requests
import urllib
import re
import MySQLdb
import time
import os

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
js = 1

asdy = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept - Encoding':'gzip, deflate, br',
               'Accept-Language':'zh-CN,zh;q=0.8',
               'Connection':'keep-alive',
               'Host':'www.booktxt.net',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36'}

xiaoshuo = "3_3490"
hurl = "https://www.booktxt.net/%s/" % (xiaoshuo)
req = requests.get(hurl, headers=asdy)
req.encoding = "gbk"
req = req.text


def sqlmulu(zjtitles,zjid):
    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sqlmulu = "INSERT INTO x_mulu(x_ids, x_zjid, x_zjnr, times) " \
          "VALUES(%s, '%s', '%s', '%s')" % (x_id, zjid, zjtitles, times)
    cursor.execute(sqlmulu)
    print zjid, zjtitles, "写入成功！", times

def sqlneirong(zjid, qx, jss):
    sqlneirong = "insert into x_neirong(x_neirong, x_zjids, ids, x_ids) values ('%s', '%s', %s, '%s')" % (zjid, qx, jss, x_id)
    cursor.execute(sqlneirong)
    print "章节写入成功！"

def sqlxiaoshuoxinxi(x_name,x_zuozhe,x_tupian, x_jianjie):
    sql = "INSERT INTO x_xiaoshuo(x_id, x_name, jianjie, x_fengmian, zuozhe, zishu) VALUES(%s, '%s', '%s', '%s', '%s', %s)" % (x_id, x_name, x_jianjie, x_tupian, x_zuozhe, zishu)
    cursor.execute(sql)
    print "小说信息获取并写入数据库成功！"


def neirong(url, title, js):
    qqiu = requests.get(hurl+url, headers=asdy)
    qqiu.encoding = "gbk"
    qqiu = qqiu.text
    nrk = r'<div id="content">(.*?)</div>'
    neirong = re.findall(nrk,qqiu)[0]
    neirong = re.sub("<br />", "\n", neirong)
    zjid = "%d%s%d" % (x_id, lj, js)
    jss = js
    titles = title
    sqlmulu(titles, zjid)
    sqlneirong(neirong, zjid, jss)

# 小说信息匹配-小说名字
pp2 = r'<meta property="og:novel:book_name" content="(.*?)"/>'
x_name = re.findall(pp2, req)[0]

# 小说信息匹配-小说作者
pp2 = r'<meta property="og:novel:author" content="(.*?)"/>'
x_zuozhe = re.findall(pp2, req)[0]

# 小说信息匹配-小说封面
pp2 = r'<meta property="og:image" content="(.*?)"/>'
x_tupian = re.findall(pp2, req)[0]

# 小说信息匹配-小说简介
pp2 = r'<meta property="og:description" content="(.*?)"/>'
x_jianjie = re.findall(pp2, req)[0]

# 提交小说信息保存数据库
sqlxiaoshuoxinxi(x_name, x_zuozhe, x_tupian, x_jianjie)
# print x_name, x_zuozhe, x_tupian, x_jianjie

pp2 = r'<dd><a href="(.*?)">(.*?)</a></dd>'
liebiao = re.findall(pp2,req)
for xurl,title in liebiao:
    neirong(xurl, title, js)
    js = js+1

print "小说下载完毕"


