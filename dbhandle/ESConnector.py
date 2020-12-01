#!/usr/bin/python3
'''
    @File        ESConnector.py
    @Author      pengsen cheng
    @Company     silence
    @CreatedDate 2017-07-26
'''

from .Connector import (
    Connector,
    valid_handler,
    exception_handler)
from elasticsearch import (
    Elasticsearch, 
    helpers, 
    ElasticsearchException)
import traceback

class ESConnector(Connector):
    def __init__(self, **args):
        super(ESConnector, self).__init__('elasticsearch', **args)
        
        if not self.closed:
            if 'host' not in self.__dict__ or not self.host:
                raise TypeError('ElasticSearch: the host has not been set in config file or parameters.')
            
            host = []
            for item in self.host.split(','): 
                p = item.split(':')
                host.append({'host': p[0], 'port': int(p[1])})
            self.host = host
                
            try:
                self.__client = Elasticsearch(self.host, timeout=60)
            except Exception as e:
                self.logger.error(traceback.format_exc().strip())
                raise e 
    
    @valid_handler
    def create(self, index, setting, force=False):
        tag = True
        try:
            if self.__client.indices.exists(index) and force:
                self.__client.indices.delete(index)
                self.__client.indices.create(index, {'settings': setting})
            elif not self.__client.indices.exists(index):
                self.__client.indices.create(index, {'settings': setting})
            else:
                self.logger.warning('The index {} has been created.'.format(index))
        except:
            self.logger.error(traceback.format_exc().strip())
            tag = False
        finally:
            return tag
    
    @valid_handler
    def map(self, index, mapping, properties):  
        tag = True
        try:
            self.__client.indices.put_mapping(mapping, {mapping: properties}, index)
        except:
            self.logger.error(traceback.format_exc().strip())
            tag = False
        finally:
            return tag
    
    @valid_handler
    @exception_handler
    def find(self, index, doc_type, dsl, source=False):
        return self.__client.search(index, doc_type, dsl, _source=source)
     
    @valid_handler
    @exception_handler
    def count(self, index, doc_type, dsl='{}'):
        return self.__client.count(index, doc_type, dsl)
    
    @valid_handler
    @exception_handler
    def scan(self, index, doc_type, dsl):
        for hit in helpers.scan(self.__client, query=dsl, index=index, doc_type=doc_type):
            yield hit
    
    @valid_handler
    @exception_handler
    def bulk(self, actions):
        return helpers.bulk(self.__client, actions, stats_only=True, raise_on_error=False, request_timeout=120)
    
    @valid_handler
    @exception_handler
    def parallel_bulk(self, actions, thread_count=4, chunk_size=500, queue_size=4):
        return helpers.parallel_bulk(self.__client, actions, thread_count=thread_count, chunk_size=chunk_size, queue_size=queue_size, stats_only=True, raise_on_error=False, request_timeout=120)

    @valid_handler
    @exception_handler
    def delete(self, index, doc_type, id):
        return self.__client.delete(index, doc_type=doc_type, id=id)
    
    @valid_handler
    @exception_handler
    def delete_by_query(self, index, doc_type, body, conflicts='proceed'):
        return self.__client.delete_by_query(index=index, doc_type=doc_type, body=body, conflicts=conflicts)

    @valid_handler
    @exception_handler
    def insert(self, index, doc_type, id, body):
        return self.__client.index(index=index, doc_type=doc_type, id=id, body=body)
        
if __name__ == '__main__':
    handle = ESConnector(host = '192.168.6.187:9200,192.168.6.188:9200,192.168.6.229:9200,192.168.6.230:9200')
    handle = ESConnector(config='../../config/dataset.yml')
#     
#     actions = []
#     
#     actions.append({'_index': 'test', '_type': 'text', '_id': '1', '_source': {'value': 7}, '_op_type': 'create'})
#     actions.append({'_index': 'test', '_type': 'text', '_id': '1', '_source': {'value': 8}, '_op_type': 'create'})
#     actions.append({'_index': 'test', '_type': 'text', '_id': '1', '_source': {'value': 9}, '_op_type': 'create'})
#     actions.append({'_index': 'test', '_type': 'text', '_id': '2', '_source': {'value': 2}, '_op_type': 'create'})
    
#     print(handle.bulk(actions))