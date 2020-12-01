from siteutil import *
from siteentity import *
import redis
import sys
import os
import time
#import psycopg2
import json
import platform
import yaml
import urllib.parse
from urllib.parse import quote
import re
import pymysql

sys.path.append(os.path.dirname(sys.path[0]))


f = None
config_name = "address.yml"

if platform.system() == 'Linux':
    project_path = os.path.abspath('..')

    config_path = project_path + "/" + config_name
    try:
        f = open(config_path, "r", encoding='UTF-8')
    except Exception as e:
        project_path = os.path.abspath(os.curdir)
        config_path = project_path + "/spiderV1/" + config_name
        f = open(config_path, "r", encoding='UTF-8')
else:
    project_path = os.path.abspath('..')

    config_path = project_path + "\\" + config_name
    try:
        f = open(config_path, "r", encoding='UTF-8')
    except Exception as e:
        project_path = os.path.abspath(os.curdir)
        config_path = project_path + "\\spiderV1\\" + config_name
        f = open(config_path, "r", encoding='UTF-8')

temp = yaml.load(f.read())
pg_config = temp["postgresql"]

redis_config = temp["redis"]

redis1=redis.StrictRedis(host=redis_config['host'],port=redis_config['port'],db=0)

def deal_web_dupefilter(web_name):
    '''
    删除一个网站对应的dupefilter

    :param web_name:
    :return:
    '''
    try:
        redis1.delete(web_name+':dupefilter')
    except Exception as e:
        print (e)

def deal_web_items(web_name):
    '''
    删除某个网站中的item
    :param web_name:
    :return:
    '''
    try:
        redis1.delete(web_name+':items')
    except Exception as e:
        print (e)

def deal_web_start_urls(web_name):
    '''
    删除某个网站的start_urls
    :param web_name:
    :return:
    '''
    try:
        redis1.delete(web_name+':spider:strat_urls')
    except Exception as e:
        print(e)

def deal_web_requests(web_name):
    '''
    删除某个网站的requests
    :param web_name:
    :return:
    '''
    try:
        redis1.delete(web_name+':requests')
    except Exception as e:
        print(e)

def clear_redis(one):
    deal_web_dupefilter(one)
    deal_web_items(one)
    deal_web_requests(one)
    deal_web_start_urls(one)

def send_all_url():
    site_arr = get_sites_info()
    site_arr_res = get_sites_info()
    site_arr = list()
    all_spiders_in_dir = list(map(lambda x: re.search(r'(.*?).py', x.strip()).group(1),
                                  filter(lambda x: x.strip()[-3:] == '.py',
                                         os.listdir('{}/spiders'.format(project_path)))))
    for site_info in site_arr_res:
        if site_info.site in all_spiders_in_dir:
            site_arr.append(site_info)


    #检索关键词列表
    key_words = list()
    moviedata = get_movieinfo()
    #检索境外网站用的关键词表
    #overseas_words = get_bigeverntsword()

    #查询重点人物的目录
    userlist = list()
    for sitebean in site_arr:
        site_name = sitebean.site
        redis_name = site_name + ":spider:strat_urls"
        if site_name == 'sinaweiboByKeyword' or site_name == 'tianyaByKeyword' or site_name == 'wechat' or site_name == 'baiduforumByKeyword':
            deal_web_dupefilter(site_name)
        if site_name == 'doubanSearch':
            for movie in moviedata:
                doubandict={}
                doubandict['name'] = movie['name']
                doubandict['id'] = movie['id']
                doubandict['type'] = movie['type']
                doubandict['sectionid'] = movie['section_id']
                jsonstr = json.dumps(doubandict).encode('utf-8')
                redis1.lpush(redis_name, jsonstr)
        else:
            index_url = sitebean.all_web_index
            if index_url is not None:
                if isinstance(index_url, list):
                    for url in index_url:
                        redis1.lpush(redis_name, url)
                else:
                    redis1.lpush(redis_name, index_url)
                print(site_name)
            # key_index = sitebean.key_index
            # if key_index is not None:
            #     key_param = sitebean.key_search_param_name
            #     #if site_name == 'sinaweibo' or site_name == 'baiduforumkey':
            #     #key_words = get_keyword()
            #     #查询通配符的个数
            #     if site_name == 'sinaweiboByKeyword':
            #         for keyword in key_words:
            #             keyword_url = "+".join(list(map(lambda x: quote(x), keyword.split(" "))))
            #             url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{0}%26t%3D0&page_type=searchall".format(
            #                 keyword_url)
            #             redis1.lpush(redis_name, url)
            #     else:
            #         key_count = word_count_in_str(key_index,'%s')
            #         print(key_count)
            #
            #         if key_count >0:
            #             for word in key_words:
            #                 if "baiduforum" in site_name:
            #                     try:
            #                         word = urllib.parse.quote(word,encoding='GBK')
            #                     except:
            #                         continue
            #                 keyparam = ''
            #                 for i in range(0, key_count):
            #                     if i == key_count-1:
            #                         keyparam += "'"+word+"'"
            #                     else:
            #                         keyparam += "'"+word+"',"
            #                 newkeyparam = eval(keyparam)
            #                 new_index = key_index % (newkeyparam)
            #                 redis1.lpush(redis_name, new_index)

                    #key_words = sitebean.key_words
                    # if isinstance(key_words, list):
                    #     if len(key_words)>0:
                    #         for word in key_words:
                    #             new_index = key_index+"&"+key_param+"="+word
                    #             redis1.lpush(redis_name, new_index)
    # if userlist:
    #     for userinfo in userlist:
    #         if "user_url" in userinfo:
    #             user_url = userinfo["user_url"]
    #             site_name = userinfo["site_name"]
    #             #暂时只爬取twitter的重点任务
    #             if site_name == "Twitter":
    #                 redis_name = "twitterKeyPerson:spider:strat_urls"
    #                 redis1.lpush(redis_name,user_url)


def word_count_in_str(string, keyword):
    return len(string.split(keyword)) - 1

def send_url(site_name):
    site_info = get_site_info(site_name)
    sitebean = Site()
    if site_info is not None:
        sitebean = site_info
        try:
            redis1.lpush(site_name+':spider:start_urls',"http://m.weibo.cn/container/getIndex?containerid=100103type%3D2%26q%3D成都")
            redis1.lpush(site_name + ':spider:start_urls',
                         "http://m.weibo.cn/container/getIndex?containerid=100103type%3D2%26q%3D人民")
        except Exception as e:
            print(e)

#查询账号信息
def get_accountinfo():
    conn = psycopg2.connect(database=pg_config["database"], user=pg_config["user"],
                            password=pg_config["password"],
                            host=pg_config["host"], port=pg_config["port"])

    sql = "SELECT a.sid,a.accid,a.uname,a.cookie,b.\"name\" FROM \"opinmonitor\".\"recomdaccount\" as a JOIN \"opinmonitor\".sites as b ON a.sid=b.\"id\" WHERE a.cookie != '' AND a.cstatus = TRUE"
    cur = conn.cursor()
    resultlist = list()
    try:
        cur.execute(sql)
        # 获取表的所有字段名称

        #rows = cur.fetchall()
        coloumns = [row[0] for row in cur.description]
        result = [[str(item) for item in row] for row in cur.fetchall()]
        resultlist= [dict(zip(coloumns, row)) for row in result]
    except Exception as ex:
        print(ex)
    finally:
        conn.close()
    return resultlist

def senderror():
    redis1.config_set("stop-writes-on-bgsave-error","no")
    #redis1.lpush("config set stop-writes-on-bgsave-error", "no")

def get_movieinfo():
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': '1234',
        'db': 'spider',
        'cursorclass': pymysql.cursors.DictCursor
    }
    db = pymysql.connect(**config)
    sql = "SELECT * FROM `movie_data` WHERE cover is null AND type in ('movie','tv') "
    cursor = db.cursor()

    try:
        cursor.execute(sql)
        datas = cursor.fetchall()
        return datas
    except:
        print("查询失败")
    finally:
        cursor.close()
        db.close()

def get_bigeverntsword():
    wordlist = list()
    wordset = set()
    conn = psycopg2.connect(database=pg_config["database"], user=pg_config["user"],
                            password=pg_config["password"],
                            host=pg_config["host"], port=pg_config["port"])
    # cur = conn.cursor()

    # 查询重点人物列表
    # sql = 'SELECT words FROM "mds9311"."kmwords" ORDER BY updatetime desc LIMIT 10 OFFSET 0'

    sql = 'SELECT words FROM "mds9311"."bigevents" WHERE "delete" is null'
    cur = conn.cursor()
    try:
        cur.execute(sql)
        # 获取表的所有字段名称

        rows = cur.fetchall()

        for row in rows:
            #words = row[0]
            # print(words)

            for key in row:
                key_param = ""
                #print(key)
                for word in key:
                    if word!='':
                        #print(word)
                        wordset.add(word)
                #wordlist.append(key_param)


            # new_words = json.dumps(eval("b"+words))
            # wordsjson = json.loads(new_words)
            # for key in wordsjson:
            #     print(key)
            #     wordlist.append(key)
        # wordlist = list(wordset)
        # coloumns = [row[0] for row in cur.description]
        # result = [[str(item) for item in row] for row in cur.fetchall()]
        # resultdic = [dict(zip(coloumns, row)) for row in result]
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return wordset

#从表中获取关键词信息
def get_keyword():
    wordlist = list()
    wordset = set()
    conn = psycopg2.connect(database=pg_config["database"], user=pg_config["user"],
                            password=pg_config["password"],
                            host=pg_config["host"], port=pg_config["port"])
    # cur = conn.cursor()

    #sql = 'SELECT words FROM "mds9311"."kmwords" ORDER BY updatetime desc LIMIT 10 OFFSET 0'

    # 查询重点人物列表
    sql = 'SELECT keys FROM "mds9311"."events" WHERE "delete" = false'
    sql1 = 'SELECT word,"user" FROM "mds9311"."basekeywords"'
    cur = conn.cursor()
    try:
        cur.execute(sql)
        # 获取表的所有字段名称

        rows = cur.fetchall()

        for row in rows:
            words = row[0]
            #print(words)

            for key in words:
                key_param = ""
                for i in range(0,len(key)):
                    if i == len(key)-1:
                        key_param += key[i]
                    else:
                        key_param += key[i]+" "
                print(key_param)
                wordlist.append(key_param)
                #wordset.add(key)
        #查询基础关键词表
        cur.execute(sql1)
        base_rows = cur.fetchall()
        for row in base_rows:
            word = row[0]
            wordlist.append(word)

            # new_words = json.dumps(eval("b"+words))
            # wordsjson = json.loads(new_words)
            # for key in wordsjson:
            #     print(key)
            #     wordlist.append(key)
        #wordlist = list(wordset)
        # coloumns = [row[0] for row in cur.description]
        # result = [[str(item) for item in row] for row in cur.fetchall()]
        # resultdic = [dict(zip(coloumns, row)) for row in result]
    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    # for row in resultdic:
    #     words = row["words"]
    #     new_words = "r"+words
    #     wordsjson = json.loads(new_words)
    #     for key in wordsjson:
    #         print(key)
    #         wordlist.append(key)

    return wordlist

def get_baseword():
    wordlist = list()
    conn = psycopg2.connect(database=pg_config["database"], user=pg_config["user"],
                            password=pg_config["password"],
                            host=pg_config["host"], port=pg_config["port"])
    sql1 = 'SELECT word,"user" FROM "mds9311"."basekeywords"'
    cur = conn.cursor()
    try:
        # 查询基础关键词表
        cur.execute(sql1)
        base_rows = cur.fetchall()
        for row in base_rows:
            word = row[0]
            user = row[1]
            if "|" in word:
                words = word.split("|")
                for wordinfo in words:
                    wordparam = {'user':user,'word':wordinfo}
                    wordlist.append(wordparam)
            else:
                wordparam = {'user': user, 'word': word}
                wordlist.append(wordparam)

    except Exception as ex:
        print(ex)
    finally:
        conn.close()

    return wordlist

def senderror():
    redis1.config_set("stop-writes-on-bgsave-error","no")
 #获取其他用户主页的url
def get_homeurl():
    userlist = list()
    conn = psycopg2.connect(database=pg_config["database"], user=pg_config["user"],
                            password=pg_config["password"],
                            host=pg_config["host"], port=pg_config["port"])
    #查询重点人物列表
    sql = 'SELECT a.*,b."name",b."type" FROM "mds9311"."keymanview" as a JOIN "mds9311".sites as b ON a.sid=b.id WHERE a."delete" = false  AND a.home is not null '
    # cursor.execute(sql)
    #
    # rows = cursor.fetchall()

    cur = conn.cursor()
    try:
        cur.execute(sql)
        # 获取表的所有字段名称
        coloumns = [row[0] for row in cur.description]
        result = [[str(item) for item in row] for row in cur.fetchall()]
        resultdic =  [dict(zip(coloumns, row)) for row in result]
    except Exception as ex:
        print(ex)
    finally:
        conn.close()


    for row in resultdic:
        user_url = row["home"]
        site_name = row["name"]
        user_name = row["nickname"]
        user_id = row["uid"]
        user_item = {"user_url":user_url,"site_name":site_name,"user_name":user_name,"uid":user_id}
        userlist.append(user_item)


    #http://www.chengdu.gov.cn
    #http://www.tianya.cn/66443816
    #useritem = {"user_url":"http://www.tianya.cn/66443816","site_name":"天涯社区"}



    #userlist.append(useritem)

    # if len(userlist)>0:
    #     for user_dic in userlist:
    #         if "site_name" in user_dic:
    #             site_name = user_dic["site_name"]
    #             sitebean = siteutil.get_sitecn_info(site_name)
    #             if sitebean is None:
    #                 logging("没有配置该网站信息:"+site_name)
    #                 break
    #             user_dic["site_en_name"]=sitebean.site
    #             user_dic["plant_type"] = sitebean.sitetype
    #             user_dic["home_splash"] = sitebean.home_splash

    return userlist

if __name__ == '__main__':
    #sys.path.append(os.path.dirname(sys.path[0]))
    #send_url("sinaweibo")
    #send_all_url()
    #senderror()
    #get_keyword()
    #get_bigeverntsword()
    #get_accountinfo()
    #wordlist = get_baseword()
    while (1 > 0):
        senderror()
        send_all_url()
        time.sleep(6*60*60)
