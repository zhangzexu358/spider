#!/usr/bin/python3
'''
    @File        MongoConnector.py
    @Author      pengsen cheng
    @Company     bhyc
    @CreatedDate 2015-12-02
'''

from .Connector import (
    Connector,
    valid_handler,
    exception_handler)
import pymongo
import traceback

class MongoConnector(Connector):
    def __init__(self, **args):
        super(MongoConnector, self).__init__('mongodb', **args)
        if not self.closed:
            if 'host' not in self.__dict__ or not self.host:
                raise TypeError('MongoDB: the host has not been set in config file or parameters.')
            if 'database' not in self.__dict__ or not self.database:
                raise TypeError('MongoDB: the database has not been set in config file or parameters.')
            if 'port' not in self.__dict__ or not self.port:
                self.port = 27017
            if 'thread' not in self.__dict__ or not self.thread:
                self.thread = 1
            if 'user' not in self.__dict__ or not self.user:
                raise TypeError('MongoDB: the user has not been set in config file or parameters.')
            if 'password' not in self.__dict__ or not self.password:
                raise TypeError('MongoDB: The password has not been set in config file or parameters.')
           
            self.uri = 'mongodb://{}:{}@{}:{}/{}'.format(self.user, self.password, self.host, self.port, self.database)
            try:
                self.__handle = pymongo.MongoClient(host=self.uri, maxPoolSize=self.thread, socketKeepAlive=True, unicode_decode_error_handler='ignore')
            except Exception as e:
                raise e
    
    def __del__(self):
        if '_MongoConnector__handle' in self.__dict__ and self.__handle:
            self.__handle.close()
    
    @valid_handler
    @exception_handler
    def find(self, database, collection_name, query={}, field=None, sort=None, skip=0, limit=10):
        db = self.__handle[database]
        for doc in db[collection_name].find(query, field, sort=sort, skip=skip, limit=limit):
            yield doc
            
    @valid_handler
    @exception_handler
    def insert(self, database, collection_name, doc):
        db = self.__handle[database]
        db[collection_name].insert_one(doc)
        return doc
    
    @valid_handler
    @exception_handler
    def update(self, database, collection_name, query, field, upsert=False):
        db = self.__handle[database]
        return db[collection_name].find_one_and_update(query, field, return_document=pymongo.ReturnDocument.AFTER)
        
    @valid_handler
    @exception_handler
    def count(self, database, collection_name, query = {}):
        db = self.__handle[database]
        return db[collection_name].count(query)
        
    @valid_handler
    @exception_handler
    def aggregate(self, database, collection_name, pipeline):
        db = self.__handle[database]
        for doc in db[collection_name].aggregate(pipeline):
            yield doc
            
    @valid_handler
    @exception_handler
    def delete(self, database, collection_name, query = {}):
        db = self.__handle[database]
        return db[collection_name].delete_many(query)
    
    @valid_handler
    @exception_handler
    def save(self, database, collection_name, doc):
        db = self.__handle[database]
        db[collection_name].save(doc)
        return doc
    
if __name__ == '__main__':
    handle = MongoConnector(host='192.168.6.186', port=27017, user='silence', password='silence', database='admin')
    
    for doc in handle.find('HINTSV2', 'GroupChat', limit=1):
        print(doc)
    
    data = handle.count('HINTSV2', 'GroupChat', {'_id': 1})
    print(data)




