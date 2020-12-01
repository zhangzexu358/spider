import sys
import os


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
        self._rules_is_body = str(value)
   
    
    
       


