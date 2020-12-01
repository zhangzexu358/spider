import os
import yaml
import sys
import platform

site_dic = {}
site_arr = list()
confpath = ''
site_cndic = {}
bingsearch_cookie =  'MUID=19D29AC63C0B625111C194E5380B61C9; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=7831BF64E4B0414986233D52F4C4181A&dmnchg=1; _SS=SID=3095E39F049D6148181EED0C05B3605D; MUIDB=19D29AC63C0B625111C194E5380B61C9; SRCHUSR=DOB=20200203&T=1584676131000; ipv6=hit=1584679741686&t=4; _EDGE_S=mkt=zh-cn&SID=3095E39F049D6148181EED0C05B3605D; SNRHOP=I=&TS=; SRCHHPGUSR=CW=1920&CH=937&DPR=1&UTC=480&HV=1584676732&WTS=63720272931'

def site_util():
    file_name = "site.yaml"
    f = None
    if platform.system() == 'Linux':
        try:
            path = os.path.abspath('..')
            file_path = path + "/"+file_name
            f = open(file_path, "r", encoding='UTF-8')
        except Exception as e:
            path = os.path.abspath(os.curdir)
            file_path = path+"/spiderV1/" + file_name
            f = open(file_path, "r", encoding='UTF-8')
    else:
        path = os.path.abspath('..')

        file_path = path + "\\" + file_name

        try:
            f = open(file_path, "r", encoding='UTF-8')
        except Exception as e:
            path = os.path.abspath(os.curdir)
            file_path = path+"\\spiderV1\\" + file_name
            f = open(file_path, "r", encoding='UTF-8')
    try:

        temp = yaml.load(f.read())
        #print(temp)
        site_config = temp["spider_config"]

        for sites_info in site_config:
            site_type = sites_info["site_type"]
            sites = sites_info["sites"]
            for site in sites:
                sitebean = Site()
                sitebean.sitetype = site_type
                site_name = site["site_name"]
                site_ename = site["site"]
                need_webdriver = site["need_webdriver"]
                need_login = site["need_login"]
                home_splash = False
                if "home_splash" in site:
                    home_splash = site["home_splash"]
                if "encoding" in site:
                    encoding = site["encoding"]
                    sitebean.encoding = encoding
                if "spider_request_type" in site:
                    spider_request_type = site["spider_request_type"]
                    sitebean.spider_request_type = spider_request_type

                if "need_proxy" in site:
                    sitebean.need_proxy = site["need_proxy"]

                sitebean.sitename=site_name
                sitebean.site=site_ename
                sitebean.need_webdriver=need_webdriver
                sitebean.need_login=need_login
                if home_splash is not None:
                    sitebean.home_splash = home_splash

                if need_login == True and "login" in site:
                    login_info = site["login"]
                    print("url_request" in login_info)
                    if "url_request" in login_info:
                        sitebean.login_type="url_request"
                        url_login_info = login_info["url_request"]
                        url_login_url = url_login_info["login_url"]
                        url_accounts = url_login_info["accounts"]
                        sitebean.url_login_url=url_login_url
                        accounts_array = list()
                        for account in url_accounts:
                            accountbean = Account()
                            user = account["user"]
                            pwd = account["pwd"]
                            accountbean.user=user
                            accountbean.pwd=pwd
                            accounts_array.append(accountbean)
                        sitebean.accounts=accounts_array
                        url_request_type = url_login_info["request_type"]
                        url_user_param_name = url_login_info["user_param_name"]
                        url_pwd_param_name = url_login_info["pwd_param_name"]
                        sitebean.url_login_request_type=url_request_type
                        sitebean.url_user_param_name=url_user_param_name
                        sitebean.url_pwd_param_name=url_pwd_param_name
                    elif "webdriver" in login_info:
                        driver_login_info = login_info["webdriver"]
                        driver_login_url = driver_login_info["login_url"]
                        driver_accounts = driver_login_info["accounts"]
                        sitebean.driver_login_url = driver_login_url
                        sitebean.login_type = "webdriver"
                        accounts_array = list()
                        for account in driver_accounts:
                            accountbean = Account()
                            user = account["user"]
                            pwd = account["pwd"]
                            accountbean.user=user
                            accountbean.pwd=pwd
                            accounts_array.append(accountbean)
                        sitebean.accounts=accounts_array
                        driver_user_param = driver_login_info["user_param"]
                        driver_pwd_param = driver_login_info["pwd_param"]
                        driver_login_param = driver_login_info["login_param"]

                        sitebean.driver_user_param=driver_user_param
                        sitebean.driver_pwd_param=driver_pwd_param
                        sitebean.driver_login_param=driver_login_param

                if "all" in site :
                    spider_type = sitebean.spider_type
                    spider_type["all"] = True
                    sitebean.spider_type=spider_type
                    all_site_info = site["all"]
                    all_spider_level = 1
                    if "spider_level" in all_site_info :
                        all_spider_level = all_site_info["spider_level"]

                    sitebean.all_spider_level=all_spider_level
                    all_rule_list = list()
                    if "rules" in all_site_info:
                        rules = all_site_info["rules"]
                        rule_arr = list()
                        for rule in rules:
                            rulebean = Rules()
                            if "allow" in rule:
                                allow = rule["allow"]
                                rulebean.rules_allow = allow
                            if "deny" in rule:
                                rulebean.rules_deny = rule["deny"]
                            if "follow" in rule:
                                rulebean.rules_follow = rule["follow"]
                            if "restrict_xpaths" in rule:
                                rulebean.rules_restrict_xpaths = rule["restrict_xpaths"]
                            if "is_body" in rule:
                                rulebean.rules_is_body = rule["is_body"]
                            rule_arr.append(rulebean)
                        sitebean.rules = rule_arr

                    if "web" in all_site_info:
                        sitebean.all_type="web"
                        all_web_info = all_site_info["web"]
                        all_web_index = all_web_info["index"]
                        if "spider_floor" in all_web_info:
                            all_web_spider_floor = all_web_info["spider_floor"]
                            sitebean.all_web_spider_floor = all_web_spider_floor
                        if "spider_range" in all_web_info:
                            all_web_spider_range = all_web_info["spider_range"]
                            sitebean.all_web_spider_range = all_web_spider_range

                        sitebean.all_web_index=all_web_index

                    elif "app" in site:
                        sitebean.all_type="app"
                        all_app_info = all_site_info["app"]
                        all_app_channels = all_app_info["channels"]


                        sitebean.all_app_channels=all_app_channels

                if "vip_user" in site:
                    spider_type = sitebean.spider_type
                    spider_type["vip_user"] = True
                    sitebean.spider_type=spider_type
                    user_info = site["vip_user"]
                    user_spider_level = 3
                    if "spider_level" in user_info:
                        user_spider_level = user_info["spider_level"]
                    if "rules" in user_info:
                        rules = user_info["rules"]
                        rule_arr = list()
                        for rule in rules:
                            rulebean = Rules()
                            if "allow" in rule:
                                allow = rule["allow"]
                                rulebean.rules_allow = allow
                            if "deny" in rule:
                                rulebean.rules_deny = rule["deny"]
                            if "follow" in rule:
                                rulebean.rules_follow = rule["follow"]
                            if "restrict_xpaths" in rule:
                                rulebean.rules_restrict_xpaths = rule["restrict_xpaths"]
                            if "is_body" in rule:
                                rulebean.rules_is_body = rule["is_body"]
                            rule_arr.append(rulebean)
                        sitebean.rules = rule_arr
                    users = user_info["users"]

                    sitebean.user_spider_level=user_spider_level
                    sitebean.user_users=users


                if "key_word" in site :
                    spider_type = sitebean.spider_type
                    spider_type["key_word"] = True
                    sitebean.spider_type=spider_type

                    key_info = site["key_word"]
                    key_spider_level = 4

                    if "rules" in  key_info:
                        rules = key_info["rules"]
                        rule_arr = list()

                        for rule in rules:
                            rulebean = Rules()
                            if "allow" in rule:
                                allow = rule["allow"]
                                rulebean.rules_allow = allow
                            if "deny" in rule:
                                rulebean.rules_deny = rule["deny"]
                            if "follow" in rule:
                                rulebean.rules_follow = rule["follow"]
                            if "restrict_xpaths" in rule:
                                rulebean.rules_restrict_xpaths = rule["restrict_xpaths"]
                            if "is_body" in rule:
                                rulebean.rules_is_body = rule["is_body"]
                            rule_arr.append(rulebean)
                        sitebean.rules = rule_arr
                    if "spider_level" in key_info:
                        key_spider_level = key_info["spider_level"]
                    key_index = key_info["index"]
                    key_words = key_info["words"]
                    key_search_param_name = ' '
                    if 'search_param_name' in key_search_param_name:
                        key_search_param_name = key_info["search_param_name"]

                    sitebean.key_spider_level=key_spider_level
                    sitebean.key_index=key_index
                    sitebean.key_words=key_words

                    sitebean.key_search_param_name=key_search_param_name
                site_arr.append(sitebean)
                site_dic[site_ename] = sitebean  #对应网站英文名称
                site_cndic[site_name] = sitebean  # 对应网站中文名称



        #print(temp["spider_config"][0]["site_type"])
        #print(temp["spider_config"][0]["sites"][0])
        #print(temp['basic_name']['test_name'])
        #print(temp['basic_name']['selected_name'][0])
    finally:
        if f is not None:
            f.close()

def get_sites_info():
    if len(site_arr)<=0:
        site_util()

    return site_arr

def get_site_info(site):
    if len(site_dic)<=0:
        site_util()

    if site in site_dic:
        return site_dic[site]
    else:
        return None

def get_searchCookie():
    cookie = 'MUID=19D29AC63C0B625111C194E5380B61C9; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=7831BF64E4B0414986233D52F4C4181A&dmnchg=1; _SS=SID=3095E39F049D6148181EED0C05B3605D; MUIDB=19D29AC63C0B625111C194E5380B61C9; SRCHUSR=DOB=20200203&T=1584676131000; ipv6=hit=1584679741686&t=4; _EDGE_S=mkt=zh-cn&SID=3095E39F049D6148181EED0C05B3605D; SNRHOP=I=&TS=; SRCHHPGUSR=CW=1920&CH=937&DPR=1&UTC=480&HV=1584676732&WTS=63720272931'
    return cookie

#根据网站中文名称获取网站信息
def get_sitecn_info(site_cn):
    if len(site_cndic)<=0:
        site_util()

    if site_cn in site_cndic:
        return site_cndic[site_cn]
    else:
        return None


if __name__ == '__main__':
    # print(os.getcwd())  # 获取当前工作目录路径
    # print(os.path.abspath('.'))  # 获取当前工作目录路径
    # print(os.path.abspath('test.txt'))  # 获取当前目录文件下的工作目录路径
    # print(os.path.abspath('..'))  # 获取当前工作的父目录 ！注意是父目录路径
    # print(os.path.abspath(os.curdir))  # 获取当前工作目录路径
    # setting = site_util()
    test = b'\xd3\xc9\xd3\xda\xc4\xbf\xb1\xea\xbc\xc6\xcb\xe3\xbb\xfa\xbb\xfd\xbc\xab\xbe\xdc\xbe\xf8\xa3\xac\xce\xde\xb7\xa8\xc1\xac\xbd\xd3\xa1\xa3'
    #str1 = test.encode("utf-8")
    u1 = test.decode("gbk","ignore")
    print(u1)


class Site():
    def __init__(self):
        self._sitetype = ''
        self._site = None
        self._sitename = None
        self._need_webdriver = False
        self._need_login = False
        self._encoding = 'utf-8'
        self._spider_request_type = 'get'
        self._login_type = None
        self._accounts = None
        self._url_login_url = None
        self._url_login_request_type = None
        self._url_user_param_name = None
        self._url_pwd_param_name = None
        self._driver_login_url = None
        self._driver_user_param = None
        self._driver_pwd_param = None
        self._driver_login_param = None
        self._spider_type = {}
        self._all_spider_level = None
        self._all_type = None
        self._all_web_index = None
        self._all_web_spider_range = None
        self._all_web_spider_floor = None
        self._all_web_request_type = None
        self._all_app_channels = None
        self._all_app_request_type = None
        self._user_spider_level = None
        self._user_users = None
        self._user_request_type = None
        self._key_spider_level = None
        self._key_index = None
        self._key_words = None
        self._key_request_type = None
        self._rules = None
        self._home_splash = False
        self._need_proxy = False

    @property
    def sitetype(self):
        return self._sitetype

    @sitetype.setter
    def sitetype(self, value):
        self._sitetype = value

    @property
    def site(self):
        return self._site

    @site.setter
    def site(self, value):
        self._site = str(value)

    @property
    def sitename(self):
        return self._sitename

    @sitename.setter
    def sitename(self, value):
        self._sitename = str(value)

    @property
    def need_webdriver(self):
        return self._need_webdriver

    @need_webdriver.setter
    def need_webdriver(self, value):
        self._need_webdriver = value

    @property
    def need_login(self):
        return self._need_login

    @need_login.setter
    def need_login(self, value):
        self._need_login = value

    @property
    def home_splash(self):
        return self._home_splash

    @home_splash.setter
    def home_splash(self, value):
        self._home_splash = value

    @property
    def spider_request_type(self):
        return self._spider_request_type

    @spider_request_type.setter
    def spider_request_type(self, value):
        self._spider_request_type = value

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, value):
        self._encoding = str(value)

    @property
    def login_type(self):
        return self._login_type

    @login_type.setter
    def login_type(self, value):
        self._login_type = str(value)

    @property
    def accounts(self):
        return self._accounts

    @accounts.setter
    def accounts(self, value):
        self._accounts = value

    @property
    def url_login_url(self):
        return self._url_login_url

    @url_login_url.setter
    def url_login_url(self, value):
        self._url_login_url = str(value)

    @property
    def url_login_request_type(self):
        return self._url_login_request_type

    @url_login_request_type.setter
    def url_login_request_type(self, value):
        self._url_login_request_type = str(value)

    @property
    def url_user_param_name(self):
        return self._url_user_param_name

    @url_user_param_name.setter
    def url_user_param_name(self, value):
        self._url_user_param_name = str(value)

    @property
    def url_pwd_param_name(self):
        return self._url_pwd_param_name

    @url_pwd_param_name.setter
    def url_pwd_param_name(self, value):
        self._url_pwd_param_name = str(value)

    @property
    def driver_login_url(self):
        return self._driver_login_url

    @driver_login_url.setter
    def driver_login_url(self, value):
        self._driver_login_url = str(value)

    @property
    def driver_user_param(self):
        return self._driver_user_param

    @driver_user_param.setter
    def driver_user_param(self, value):
        self._driver_user_param = str(value)

    @property
    def driver_pwd_param(self):
        return self._driver_pwd_param

    @driver_pwd_param.setter
    def driver_pwd_param(self, value):
        self._driver_pwd_param = str(value)

    @property
    def driver_login_param(self):
        return self._driver_login_param

    @driver_login_param.setter
    def driver_login_param(self, value):
        self._driver_login_param = str(value)

    @property
    def spider_type(self):
        return self._spider_type

    @spider_type.setter
    def spider_type(self, value):
        self._spider_type = value

    @property
    def all_spider_level(self):
        return self._all_spider_level

    @all_spider_level.setter
    def all_spider_level(self, value):
        self._all_spider_level = value

    @property
    def all_type(self):
        return self._all_type

    @all_type.setter
    def all_type(self, value):
        self._all_type = value

    @property
    def all_web_index(self):
        return self._all_web_index

    @all_web_index.setter
    def all_web_index(self, value):
        self._all_web_index = value

    @property
    def all_web_spider_range(self):
        return self._all_web_spider_range

    @all_web_spider_range.setter
    def all_web_spider_range(self, value):
        self._all_web_spider_range = value

    @property
    def all_web_spider_floor(self):
        return self._all_web_spider_floor

    @all_web_spider_floor.setter
    def all_web_spider_floor(self, value):
        self._all_web_spider_floor = value

    @property
    def all_web_request_type(self):
        return self._all_web_request_type

    @all_web_request_type.setter
    def all_web_request_type(self, value):
        self._all_web_request_type = str(value)

    @property
    def all_app_channels(self):
        return self._all_app_channels

    @all_app_channels.setter
    def all_app_channels(self, value):
        self._all_app_channels = value

    @property
    def all_app_request_type(self):
        return self._all_app_request_type

    @all_app_request_type.setter
    def all_app_request_type(self, value):
        self._all_app_request_type = str(value)

    @property
    def user_spider_level(self):
        return self._user_spider_level

    @user_spider_level.setter
    def user_spider_level(self, value):
        self._user_spider_level = value

    @property
    def user_users(self):
        return self._user_users

    @user_users.setter
    def user_users(self, value):
        self._user_users = value

    @property
    def user_request_type(self):
        return self._user_request_type

    @user_request_type.setter
    def user_request_type(self, value):
        self._user_request_type = str(value)

    @property
    def key_spider_level(self):
        return self._key_spider_level

    @key_spider_level.setter
    def key_spider_level(self, value):
        self._key_spider_level = value

    @property
    def key_index(self):
        return self._key_index

    @key_index.setter
    def key_index(self, value):
        self._key_index = str(value)

    @property
    def key_words(self):
        return self._key_words

    @key_words.setter
    def key_words(self, value):
        self._key_words = value

    @property
    def key_request_type(self):
        return self._key_request_type

    @key_request_type.setter
    def key_request_type(self, value):
        self._key_request_type = str(value)

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        self._rules = value

    @property
    def need_proxy(self):
        return self._need_proxy

    @need_proxy.setter
    def need_proxy(self, value):
        self._need_proxy = value


class Account():
    def __init__(self):
        self._user = None
        self._pwd = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = str(value)

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, value):
        self._pwd = str(value)


class Rules():
    def __init__(self):
        self._rules_allow = None
        self._rules_deny = None
        self._rules_follow = False
        self._rules_restrict_xpaths = None
        self._rules_is_body = True

    @property
    def rules_allow(self):
        return self._rules_allow

    @rules_allow.setter
    def rules_allow(self, value):
        self._rules_allow = str(value)

    @property
    def rules_deny(self):
        return self._rules_deny

    @rules_deny.setter
    def rules_deny(self, value):
        self._rules_deny = str(value)

    @property
    def rules_follow(self):
        return self._rules_follow

    @rules_follow.setter
    def rules_follow(self, value):
        self._rules_follow = value

    @property
    def rules_restrict_xpaths(self):
        return self._rules_restrict_xpaths

    @rules_restrict_xpaths.setter
    def rules_restrict_xpaths(self, value):
        self._rules_restrict_xpaths = str(value)

    @property
    def rules_is_body(self):
        return self._rules_is_body

    @rules_is_body.setter
    def rules_is_body(self, value):
        self._rules_is_body = value

