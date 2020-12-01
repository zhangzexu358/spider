#!/usr/bin/python3
'''
    @File        ESConnector.py
    @Author      pengsen cheng
    @Company     silence
    @CreatedDate 2017-07-26
'''
import os
import traceback
import yaml


def valid_handler(func):
    def wrapper(self, *args, **kwargs):
        if self.closed:
            return {'error': 'service has closed the related functions. please contact the manager.'}
        return func(self, *args, **kwargs)
        
    wrapper.__name__ = func.__name__
    return wrapper
    
def exception_handler(func):
    def wrapper(self, *args, **kwargs):
        try:
            data = func(self, *args, **kwargs)
        except Exception as e:
            #self.logger.error(traceback.format_exc().strip())
            data = {'error': str(e)}
            print(e)
        finally:
            return data
    wrapper.__name__ = func.__name__
    return wrapper


class Connector(object):
    def __parsexml(self, file, dbtype):
        path = os.path.abspath('..')
        file_path = path + "\\" + file

        f = None
        try:
            f = open(file_path, "r", encoding='UTF-8')
        except Exception as e:
            path = os.path.abspath(os.curdir)
            file_path = path + "\\spiderV1\\" + file
            f = open(file_path, "r", encoding='UTF-8')

        temp = yaml.load(f.read())
        kafka_config = temp[dbtype]

        # tree = ElementTree.ElementTree(file=file)
        # nodes = tree.getroot().find(dbtype)
        nodes = kafka_config[dbtype]
        if not nodes:
            self.logger.warning('{} has not been set. service closes the related functions'.format(dbtype))
            self.closed = True
            
        for node in nodes:    
            self.__setattr__(node.tag.lower(), node.text)
            
    def __parseyml(self, file, dbtype):
        path = os.path.abspath('..')
        file_path = path + "\\" + file

        f = None
        try:
            f = open(file_path, "r", encoding='UTF-8')
        except Exception as e:
            path = os.path.abspath(os.curdir)
            file_path = path + "\\spiderV1\\" + file
            f = open(file_path, "r", encoding='UTF-8')

        temp = yaml.load(f.read())
        kafka_config = temp["kafka"]


        with open(file) as fp:
            config = yaml.load(fp)
            
        if dbtype not in config:
            self.logger.warning('{} has not been set. service closes the related functions'.format(dbtype))
            self.closed = True
            
        for k, v in config[dbtype].items():
            self.__setattr__(k, v)
                
    def __init__(self, dbtype, **args):         
        self.closed = False
        #self.logger = StdOut(dbtype)
        
        if 'config' in args:
            if os.path.splitext(args['config'])[-1] == '.xml':
                self.__parsexml(args['config'], dbtype)
            else:
                self.__parseyml(args['config'], dbtype)
        
        for k, v in args.items():
            if k == 'config':
                continue
            self.__setattr__(k, v)
