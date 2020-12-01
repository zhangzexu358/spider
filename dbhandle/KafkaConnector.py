#!/usr/bin/python3
'''
    @File        KafkaConnector.py
    @Author      pengsen cheng
    @Company     silence
    @CreatedDate 2017-07-21
'''
import kafka
import pykafka
import json 
import traceback 
import time
from .Connector import (
    Connector,
    valid_handler,
    exception_handler)

class Producer(Connector):
    def __init__(self, **args):
        super(Producer, self).__init__('kafka', **args)
        if not self.closed:
            if 'host' not in self.__dict__ or not self.host:
                raise TypeError('KAFKA: the host has not been set in config file or parameters.')
            self.host = self.host.split(',')    
            
            self.__producer = kafka.KafkaProducer(bootstrap_servers=self.host, 
                                                  max_request_size=67108864,
                                                  buffer_memory=134217728,
                                                  partitioner=kafka.partitioner.RoundRobinPartitioner(),
                                                  batch_size=32)
    
    def __del__(self):
        if '_Producer__producer' not in self.__dict__ and self.__producer:
            self.__producer.close()    
    
    @valid_handler
    #@exception_handler
    def send(self, topic, value, key=None):
        if isinstance(key, str):
            key = key.encode()
            #msgpack.packb(value)
        try:
            self.__producer.send(topic, value=value, key=key)
        except Exception as e:
            print(e)

class Consumer(Connector):
    def __init__(self, topic, group_id, **args):
        super(Consumer, self).__init__('kafka', **args)
        if not self.closed:
            if 'host' not in self.__dict__ or not self.host:
                raise TypeError('KAFKA: the host has not been set in config file or parameters.')
            if 'zookeeper' not in self.__dict__ or not self.zookeeper:
                raise TypeError('KAFKA: the zookeeper has not been set in config file or parameters.')
         
            self.__client = pykafka.KafkaClient(hosts=self.host, zookeeper_hosts=self.zookeeper)
            self.__consumer = self.__client.topics[topic.encode()].get_balanced_consumer(consumer_group=group_id.encode(), 
                                                                                auto_commit_enable=True,
                                                                                fetch_message_max_bytes=67108864)
    
    def __del__(self):
        pass

    @valid_handler
    @exception_handler
    def poll(self):
        try:
            for msg in self.__consumer:
                #print(msg.value)
                #msgpack.unpackb(msg.value, encoding='utf8')
                yield {'key': msg.partition_key, 'value': msg.value}
        except KeyboardInterrupt:
            pass
        except Exception as e:
            raise e
        finally:
            self.__consumer.stop()
            

if __name__ == '__main__':
    hosts = '192.168.6.187:9092,192.168.6.188:9092,192.168.6.229:9092'
    zookeepers = '192.168.6.187:2181,192.168.6.188:2181,192.168.6.229:2181'

    # p = Producer(host = hosts)
    # #
    # p.send('test99877', "{'cps': 5584}", '5')
    # p.send('test99877', "{'cps': 6685}", '6')
    # p.send('test99877', "{'cps': 7752}", '7')
     
    c = Consumer('zzxx', '545641654', host = hosts, zookeeper = zookeepers)
    for message in c.poll():
        print(message)
        #print("1")
