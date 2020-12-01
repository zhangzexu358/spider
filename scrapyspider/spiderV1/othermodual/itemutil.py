# from othermodual.regexutil import *
import datetime
import time
import re


# 解析言论相关数据
def speechcrawler(loader1, content_obj):
    #数据为空时赋值
    img_arr_urls = list()
    video_arr_urls = list()
    like_arr_nodes = list()
    renodes_arr = list()

    if "content" in content_obj:
        content = content_obj["content"]
        #content = "".join(content.split())
        pattern = re.compile(r'<[^>]+>|{[^>]+}|(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', re.S)
        result = pattern.sub('', content)
        result = result.replace("\r\n", "")
        result = result.replace("\t", "")
        result = result.replace("\n", "")
        result = result.replace("\'", "")
        result = result.strip()
        if result == '':
            result = ' '
        loader1.add_value('content', result)
    else:
        loader1.add_value('content'," ")
    if "id" in content_obj:
        id = content_obj["id"]
        if "." in id:
            id = id.split(".")[0]
        if "?" in id:
            id = id.split("?")[0]
        loader1.add_value('id', id)
    if "__URLID" in content_obj:
        id = content_obj["__URLID"]
        if "." in id:
            id = id.split(".")[0]
        if "?" in id:
            id = id.split("?")[0]
        loader1.add_value('id', id)
    if "img_urls" in content_obj:
        img_urls = content_obj["img_urls"]
        if len(img_urls) > 0:
            loader1.add_value('imgurls', img_urls)
        # else:
        #     loader1.add_value('imgurls','')
    # else:
    #     loader1.add_value('imgurls', '')
    if "video_urls" in content_obj:
        video_urls = content_obj["video_urls"]
        if len(video_urls) > 0:
            loader1.add_value('vidurls', video_urls)
    #     else:
    #         loader1.add_value('vidurls', ' ')
    # else:
    #     loader1.add_value('vidurls', ' ')

    if "publish_time" in content_obj:
        publish_time = content_obj["publish_time"]
        loader1.add_value('pubtime', publish_time)
    else:
        publish_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        loader1.add_value('pubtime', publish_time)

    if "publish_user" in content_obj:
        publish_user = content_obj["publish_user"]
        if publish_user == '':
            loader1.add_value('uname',' ')
        else:
            loader1.add_value('uname', publish_user)
    else:
        loader1.add_value('uname', ' ')


    if "publish_user_id" in content_obj:
        publish_user_id = content_obj["publish_user_id"]
        loader1.add_value('uid', publish_user_id)
    else:
        loader1.add_value('uid', ' ')

    if "publish_user_url" in content_obj:
        publish_user_url = content_obj["publish_user_url"]
        # loader1.add_value('publish_user_url', publish_user_url)
    if "read_count" in content_obj:
        read_info = content_obj["read_count"]
        read_count = int(getNum(read_info))
        loader1.add_value('readnum', read_count)
    else:
        loader1.add_value('readnum', 0)

    if "title" in content_obj:
        title = content_obj["title"]
        result = title.replace("\r\n", "")
        result = result.replace("\t", "")
        result = result.replace("\n", "")
        result = result.replace("\'", "")
        result = result.strip()
        loader1.add_value('title', result)
    else:
        loader1.add_value('title', ' ')
    if "publish_user_photo" in content_obj:
        loader1.add_value("pubphoto", content_obj["publish_user_photo"])
    else:
        loader1.add_value("pubphoto", ' ')
    if "like_count" in content_obj:
        like_info = content_obj["like_count"]
        like_count = int(getNum(like_info))
        loader1.add_value('likecount', like_count)
        loader1.add_value('agrcount', like_count)
    else:
        loader1.add_value('likecount', 0)
        loader1.add_value('agrcount', 0)

    if "pujsonid" in content_obj:
        loader1.add_value("pujsonid", content_obj["pujsonid"])
    else:
        loader1.add_value("pujsonid", ' ')
    if "reproduce_count" in content_obj:
        reproduce_info = content_obj["reproduce_count"]
        reproduce_count = int(getNum(reproduce_info))
        loader1.add_value('reprocnt', reproduce_count)
    else:
        loader1.add_value('reprocnt', 0)

    if "dislike_count" in content_obj:
        dislike_info = content_obj["dislike_count"]
        dislike_count = int(getNum(dislike_info))
        loader1.add_value('discount', dislike_count)
    else:
        loader1.add_value('discount', 0)

    if "like_nodes" in content_obj:
        loader1.add_value('likenode', content_obj["like_nodes"])
    # else:
    #     loader1.add_value('likenode',' ')

    if "spider_time" in content_obj:
        loader1.add_value('uptime', content_obj["spider_time"])
        loader1.add_value('ctime', content_obj["spider_time"])
    else:
        spider_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        loader1.add_value('uptime', spider_time)
        loader1.add_value('ctime', spider_time)

    if "area" in content_obj:
        loader1.add_value('area',content_obj["area"])
    else:
        loader1.add_value('area', ' ')

    if "reproduce_nodes" in content_obj:
        loader1.add_value('renodes',content_obj["reproduce_nodes"])
    # else:
    #     loader1.add_value('renodes', ' ')

    loader1.add_value('sement',0)

    loader1.add_value("data_type", "speech")

    item = loader1.load_item()


def userCrawler(loader1, content_obj):


    if "publish_user" in content_obj:
        loader1.add_value("uname", content_obj["publish_user"])
    else:
        loader1.add_value("uname", ' ')
    if "publish_user_photo" in content_obj:
        loader1.add_value("pubphoto", content_obj["publish_user_photo"])
    else:
        loader1.add_value("pubphoto", ' ')
    # if "publish_user_id" in content_obj:
    #     loader1.add_value("publish_user_id", content_obj["publish_user_id"])
    if "fans_count" in content_obj:
        fans_info = content_obj["fans_count"]
        fans_count = int(getNum(fans_info))
        loader1.add_value("fanscnt", fans_count)
    else:
        loader1.add_value("fanscnt", 0)
    if "follow_count" in content_obj:
        follow_info = content_obj["follow_count"]
        follow_count = int(getNum(follow_info))
        loader1.add_value("folwcont", follow_count)
    else:
        loader1.add_value("folwcont", 0)
    if "friend_count" in content_obj:
        friend_info = content_obj["friend_count"]
        friend_count = int(getNum(friend_info))
        loader1.add_value("fricnt", friend_count)
    else:
        loader1.add_value("fricnt", 0)
    if "sex" in content_obj:
        loader1.add_value("sex", content_obj["sex"])
    else:
        loader1.add_value("sex", ' ')
    if "register_time" in content_obj:
        loader1.add_value("regtime", content_obj["register_time"])
    else:
        loader1.add_value("regtime", 0)
    if "article_count" in content_obj:
        article_info = content_obj["article_count"]
        ariclie_count = int(getNum(article_info))
        loader1.add_value("artcont", ariclie_count)
    else:
        loader1.add_value("artcont", 0)
    if "reply_article_count" in content_obj:
        reply_article_info = content_obj["reply_article_count"]
        reply_article_count = int(getNum(reply_article_info))
        loader1.add_value("reparcnt", reply_article_count)
    else:
        loader1.add_value("reparcnt", 0)
    if "visit_count" in content_obj:
        visit_info = content_obj["visit_count"]
        visit_count = int(getNum(visit_info))
        loader1.add_value("visitcnt", visit_count)
    else:
        loader1.add_value("visitcnt", 0)
    if "group_name" in content_obj:
        loader1.add_value("groname", content_obj["group_name"])
    else:
        loader1.add_value("groname", ' ')
    if "introduction" in content_obj:
        loader1.add_value("introtion", content_obj["introduction"])
    else:
        loader1.add_value("introtion", ' ')
    if "fans_details" in content_obj:
        loader1.add_value("fandetl", content_obj["fans_details"])
    # else:
    #     loader1.add_value("fandetl", ' ')
    if "follow_details" in content_obj:
        loader1.add_value("folwdetl", content_obj["follow_details"])
    # else:
    #     loader1.add_value("folwdetl", ' ')
    if "friend_details" in content_obj:
        loader1.add_value("fridetil", content_obj["friend_details"])
    # else:
    #     loader1.add_value("fridetil", ' ')

    if "area" in content_obj:
        loader1.add_value('area', content_obj["area"])
    else:
        loader1.add_value('area', ' ')

    loader1.add_value("data_type", "user")


def getTime(timestr):
    parttern = '(\\d{1,4}[-|\\/|年|\\.]\\d{1,2}[-|\\/|月|\\.]\\d{1,2}([日|号])?(\\s)*(\\d{1,2}([点|时])?((:)?\\d{1,2}(分)?((:)?\\d{1,2}(秒)?)?)?)?(\\s)*(PM|AM)?)'


def getNum(numstr):
    try:
        parttern = '[1-9]\d*'

        test = re.compile(parttern).findall(str(numstr))[0]
        if "万" in str(numstr):
            test = int(test)*10000
        return int(test)

    except Exception as e:
        print(e)
        return 0


# 根据url获取默认id
def getdefaultId(url):
    new_obj = url.split("/")[len(url.split("/")) - 1]
    if "." in new_obj:
        new_obj = new_obj.split(".")[0]
    return new_obj


if __name__ == '__main__':
    # str1 = b'\xd3\xc9\xd3\xda\xc4\xbf\xb1\xea\xbc\xc6\xcb\xe3\xbb\xfa\xbb\xfd\xbc\xab\xbe\xdc\xbe\xf8\xa3\xac\xce\xde\xb7\xa8\xc1\xac\xbd\xd3\xa1\xa3.\r\nConnection'
    # new_str = str1.decode("gbk",'ignore')
    # print(new_str)
    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    content = '''
        \r\n\t\t\t\t\t\xa0\xa0  【再回头只能怀念】\xa0\xa0\xa0\xa0https://v.youku.com/v_show/id_XMjU1MzUzMjI0.html?from=s1.8-1-1.2&spm=a2h0k.8191407.0.0\xa0\xa0\xa0\xa0https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd=%E5%BF%83%E8%A6%81%E8%AE%A9%E4%BD%A0%E5%90%AC%E8%A7%81&rsv_pq=cf1f342b00013775&rsv_t=86d0pYeEQnSbretL%2By5bMrTD7zp0r71ATBEp15CvBO%2BSSjPKH9n81WgW%2F1Y&rqlang=cn&rsv_enter=1&rsv_sug3=1\xa0\xa0\xa0\xa0邰正宵-心要让你听见\xa0\xa0\xa0\xa0缘份让你我擦肩\xa0\xa0\xa0\xa0没开口却有感觉\xa0\xa0\xa0\xa0爱情最害怕犹豫\xa0\xa0\xa0\xa0再回头只能怀念\xa0\xa0\xa0\xa0寂寞因你而强烈\xa0\xa0\xa0\xa0熬不过漫长午夜\xa0\xa0\xa0\xa0天涯挡不住思念\xa0\xa0\xa0\xa0渴望着他年他日再相见\xa0\xa0\xa0\xa0到那天\xa0\xa0\xa0\xa0绝不再让你走过我身边\xa0\xa0  沉默的习惯 愿为你改变\r\n\t\t    \t\t
    '''
    #pattern = re.compile(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b|pic\.twitter\.com.*', re.S)
    pattern = re.compile(r'<[^>]+>|{[^>]+}|(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%|-)*\b', re.S)
    result = pattern.sub('', content)
    result = result.replace("\r\n", "")
    result = result.replace("\t", "")
    result = result.replace("\n", "")
    result = result.replace("\'", "")
    if result == '':
        result = ' '
    print(result)