# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import time
import os
import re
import yaml
import platform
import requests
import datetime
import traceback
import pymysql


BASIC_FILE="E:/data_ll2"
BASIC_FILE2='E:/data_ll2_all'
url_post='http://192.168.0.82:2348/mapDatas'
if platform.system()=='Linux':#BigDATA's workstation
    BASIC_FILE='/home/crawler/silence/spider_test/spider_content'
    BASIC_FILE2='/home/crawler/silence/spider_test/spider_content_all'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
logname = "/log/data_to_file_%s.log" % time.strftime('%Y-%m-%d', time.localtime(time.time()))
#logging.basicConfig(filename=logname, level=logging.WARNING, format=LOG_FORMAT, datefmt=DATE_FORMAT)



class ScrapytestPipeline(object):
    def process_item(self, item, spider):
        return item

class SaveDataToFile(object):
    '''
        文件存储模块，将解析出来的数据以json的格式存储到硬盘中去，路径最上边的BASIC_FILE，不是BASIC_FILE2，BASIC_FILE2在save_data_to_RemoteFile_XMX中。
    '''

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
    f.close()
    mysql_config = temp["mysql"]
    config = {
        'host': mysql_config['host'],
        'port': mysql_config['port'],
        'user': mysql_config['user'],
        'passwd': mysql_config['password'],
        'db': mysql_config['database'],
        'cursorclass': pymysql.cursors.DictCursor
    }

    def process_item(self, item, spider):
        '''
        标准的middleware函数，具体参考官方文档。
        :param item: 从spider中解析出来的对象，或者从其它middleware中解析出来的item，具体顺序可以在setting中设置，详细参见官方帮助文档。
        :param spider: spider的名称，可以提取spider中的某些字段，比如spdier_name
        :return: 这里没有返回对象，直接存储到了本地文件中。   如有需要，具体如何返回数据，参见官方文档。
        '''
        type = item["data_type"]
        if type == "movie" or type=="game":
            item_dict = dict(item)
            publishdate = item_dict["publishdate"]
            timeStruct = time.strptime(publishdate, '%Y-%m-%d')
            dstTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStruct)
            item_dict["publishdate"] = dstTime
            self.save_moviedata(item_dict=item_dict)
        elif type == 'section':
            item_dict = dict(item)
            self.save_sectiondata(item_dict=item_dict)
        return item


    def examing_datetime_format(self, timestr):
        '''
        检测时间格式是否符合规定的一个函数。因为在实际情况中，有些网页解析出来的时间格式不对，情况比较多，因为要在文件名中用到这个字段所以这个字段比较重要，
        所以这里单独设置一个模块用来处理这些意外情况。有些网站没有publish_time，跟大数据商量好了，一律使用2018-02-01 00:00:00

        :param timestr: publsh_time
        :return: 处理过后的publish_time
        '''
        try:
            if isinstance(timestr, int):
                if len(str(timestr)) == 13:
                    timestr = str(timestr)[:-3]
                timestamp = float(timestr)
                timeinfo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
                timestrlist = time.strptime(timeinfo, "%Y-%m-%d %H:%M:%S")
                return timestrlist

            else:
                timestrlist = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
                return timestrlist
        except:
            try:
                timestr = timestr.split(".")[0]
                timestrlist = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
                return timestrlist
            except:
                try:
                    timestrlist = time.strptime(timestr, '%Y-%m-%d %H:%M')
                    return timestrlist
                except:
                    try:
                        timestrlist = time.strptime(timestr, "%Y-%m-%d")
                        return timestrlist
                    except:
                        print('时间格式有误')
                        print(timestr)
                        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        timestrlist = time.strptime(now,"%Y-%m-%d %H:%M:%S")
                        return timestrlist

    def save_moviedata(self,item_dict):

        db = pymysql.connect(**self.config)
        sql = 'SELECT name FROM movie_data WHERE name = %s AND type=%s'
        sqlinsert = "INSERT INTO movie_data(id,rate,url,name,tags,cover,is_new,intro,publishdate,type,platforms,section_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sqlupdate = "UPDATE movie_data SET section_id=%s,intro=%s,tags=%s,publishdate=%s,url=%s,cover=%s,is_new=%s,rate=%s WHERE name = %s AND type=%s"

        cursor = db.cursor()

        tags = item_dict['tags']
        platforms = item_dict["platforms"]
        tagsinfo = ""
        if tags != "":
            tagsinfo = json.dumps(tags)
        sectionid = ""
        if "sectionid" in item_dict:
            sectionid = item_dict["sectionid"]
        platforminfo = ""
        if platforms != "":
            platforminfo = json.dumps(platforms)
        is_new = item_dict["is_new"]
        is_new_info =0
        if is_new == True:
            is_new_info = 1
        try:
            type = item_dict["type"]
            name = item_dict["name"]
            cursor.execute(sql, (name,type))
            datas = cursor.fetchall()
            if len(datas) <= 0:
                cursor.execute(sqlinsert, (item_dict["id"],item_dict["rate"],item_dict["url"],item_dict["name"],tagsinfo,item_dict["cover"],is_new_info,item_dict["intro"],item_dict["publishdate"],item_dict["type"],platforminfo,sectionid))
                db.commit()
            else:
                cursor.execute(sqlupdate,(sectionid,item_dict["intro"],tagsinfo,item_dict["publishdate"],item_dict["url"],item_dict["cover"],0,item_dict["rate"],name,type))
                db.commit()
        except:
            print("插入失败")
            traceback.print_exc()
        finally:
            cursor.close()
            db.close()

    def save_sectiondata(self,item_dict):
        db = pymysql.connect(**self.config)
        cursor = db.cursor()
        # db = pymysql.connect(mysql_config["host"], mysql_config["user"], mysql_config["password"], mysql_config["database"])
        section_name = item_dict["sectionName"]
        sql = "SELECT section_id FROM sections WHERE section_name = %s"

        sqlinsert = "INSERT INTO sections(section_id,section_name,section_img) VALUES(%s,%s,%s)"

        try:
            cursor.execute(sql,(item_dict["sectionName"]))
            datas = cursor.fetchall()
            if len(datas)<=0:
                cursor.execute(sqlinsert,(item_dict["sectionId"],item_dict["sectionName"],item_dict["sectionImg"]))
                db.commit()
        except:
            print("查询出错")
            traceback.print_exc()
        finally:
            cursor.close()
            db.close()

    def getTime(self,timestr):
        parttern = '(\\d{1,4}[-|\\/|年|\\.]\\d{1,2}[-|\\/|月|\\.]\\d{1,2}([日|号])?(\\s)*(\\d{1,2}([点|时])?((:)?\\d{1,2}(分)?((:)?\\d{1,2}(秒)?)?)?)?(\\s)*(PM|AM)?)'

    def getNum(self,numstr):
        try:
            parttern = '[1-9]\d*'
            test = re.compile(parttern).findall(numstr)[0]
            return test
        except Exception as e:
            print(e)
            return 0

