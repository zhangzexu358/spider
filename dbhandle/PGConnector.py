#!/usr/bin/python3
'''
    @File        PGConnector.py
    @Author      pengsen cheng
    @Company     silence
    @CreatedDate 2018-10-23
'''

from .Connector import (
    Connector,
    valid_handler,
    exception_handler)
from psycopg2 import (
    pool,
    extras,
    sql)
import traceback

class Conn(object):
    def __init__(self, handle):
        self.handle = handle
    
    def __enter__(self):
        self.conn = self.handle.getconn()
        return self.conn
    
    def __exit__(self, *args):
        self.conn.commit()
        self.handle.putconn(self.conn)

class PGConnector(Connector):
    def __init__(self, **args):
        super(PGConnector, self).__init__('postgresql', **args)
        if not self.closed:
            if 'host' not in self.__dict__ or not self.host:
                raise TypeError('Postresql: the host has not been set in config file or parameters.')
            if 'database' not in self.__dict__ or not self.database:
                raise TypeError('Postresql: the database has not been set in config file or parameters.')
            if 'port' not in self.__dict__ or not self.port:
                self.port = 5432
            if 'thread' not in self.__dict__ or not self.thread:
                self.thread = 1
            if 'user' not in self.__dict__ or not self.user:
                raise TypeError('Postresql: the user has not been set in config file or parameters.')
            if 'password' not in self.__dict__ or not self.password:
                raise TypeError('Postresql: The password has not been set in config file or parameters.')
           
            try:
                self.__handle = pool.ThreadedConnectionPool(1, 
                                                            self.thread, 
                                                            dbname=self.database, 
                                                            user=self.user, 
                                                            password=self.password, 
                                                            host=self.host, 
                                                            port=self.port, 
                                                            cursor_factory=extras.RealDictCursor)
            except Exception as e:
                raise e
            
    def __del__(self):
        if '_PGConnector__handle' in self.__dict__ and self.__handle:
            self.__handle.closeall()
        
    def __where(self, query):
        values = {}
    
        def suffix(no=[0]):
            no[0] += 1
            return str(no[0])
        
        def build_range(column, obj):
            parts = []
            for sign, v in obj.items():
                col = column + suffix()
                parts.append(sql.SQL('{}{}{}').format(sql.Identifier(column), sql.SQL(sign), sql.Placeholder(col)))
                values[col] = v
            return sql.SQL(' AND ').join(parts)    
        
        def build_enum(column, obj):
            col = column + suffix()
            if isinstance(obj, list) and len(obj) == 1:
                obj = obj[0]
        
            values[col] = obj
            if isinstance(obj, list):
                return sql.SQL('{}=ANY({})').format(sql.Identifier(column), sql.Placeholder(col)) 
            elif isinstance(obj, tuple):
                return sql.SQL('{}@>{}').format(sql.Identifier(column), sql.Placeholder(col)) 
            elif obj == None:
                return sql.SQL('{} IS {}').format(sql.Identifier(column), sql.Placeholder(col)) 
            else:
                return sql.SQL('{}={}').format(sql.Identifier(column), sql.Placeholder(col)) 

        def proc_list(column, array):
            range_items = []
            set_items = []
            for item in array:
                if isinstance(item, dict):
                    range_items.append(item)
                else:
                    set_items.append(item)
            parts = []
            if set_items:
                parts.append(build_enum(column, set_items))
            for item in range_items:
                parts.append(build_range(column, item))            
            return sql.SQL('({})').format(sql.SQL(' OR ').join(parts))  

        def build_where(conditions):
            parts = []
            for key, value in conditions.items():
                if (isinstance(value, dict) or isinstance(value, list)) and not value:
                    continue
                if key in {'AND', 'OR', 'NOT'}:
                    children = build_where(value)
                    if not children:
                        continue
                    if key == 'AND':
                        parts.append(sql.SQL(' AND ').join(children))
                    elif key == 'OR':
                        parts.append(sql.SQL('({})').format(sql.SQL(' OR ').join(children)))
                    else:
                        parts.append(sql.SQL('NOT({})').format(sql.SQL(' OR ').join(children)))
                elif isinstance(value, list):
                    parts.append(proc_list(key, value))
                elif isinstance(value, dict):
                    parts.append(build_range(key, value))
                else:
                    parts.append(build_enum(key, value))
            
            return parts
        
        parts = build_where(query)
        parts.append(sql.SQL('1=1'))
        return sql.SQL(' AND ').join(parts), values
    
 
    @valid_handler
    @exception_handler
    def find(self, scheme, table, query={}, columns='*', sort=[], skip=0, limit=10):
        print(query)
        where, values = self.__where(query)
        cmd = sql.SQL('SELECT {} FROM {}.{} WHERE {}').format(
            columns == '*' and sql.SQL(columns) or sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.Identifier(scheme),
            sql.Identifier(table),
            where)
        if sort:
            order = sql.SQL('{} {}').format(sql.Identifier(sort[0][0]), sql.SQL(sort[0][1]))
            for item in sort[1:]:
                order = sql.SQL('{}, {} {}').format(order, sql.Identifier(item[0]), sql.SQL(item[1]))
            cmd = sql.SQL('{} ORDER BY {}').format(cmd, order)
        
        cmd = sql.SQL('{} LIMIT {} OFFSET {}').format(cmd, sql.Placeholder('_limit'), sql.Placeholder('_skip'))
        values['_skip'] = skip * limit
        values['_limit'] = limit

        with Conn(self.__handle) as conn:
            with conn.cursor() as cur:
                cur.execute(cmd, values)
                print(cur.query)
                for row in cur:
                    yield row

    @valid_handler
    @exception_handler        
    def save(self, scheme, table, row, upsert=False):
        if 'id' not in row:
            raise ValueError('column id is missing')
        
        delcmd = sql.SQL('DELETE FROM {}.{} WHERE {}={}').format(
            sql.Identifier(scheme),
            sql.Identifier(table),
            sql.Identifier('id'),
            sql.Placeholder('id')
            )
        
        inscmd = sql.SQL('INSERT INTO {}.{} ({}) VALUES ({}) RETURNING *').format(
            sql.Identifier(scheme),
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, row.keys())),
            sql.SQL(', ').join(map(sql.Placeholder, row.keys()))
            )
        
        with Conn(self.__handle) as conn:
            with conn.cursor() as cur:
                cur.execute(delcmd, row)
                print(upsert)
                if cur.rowcount == 0 and not upsert:
                    raise ValueError('the data (id:{}) is not existed'.format(row['id']))
                    
                cur.execute(inscmd, row)
                return cur.fetchone()

    @valid_handler
    @exception_handler          
    def count(self, scheme, table, query={}, column='*'):
        where, values = self.__where(query)
        cmd = sql.SQL('SELECT COUNT({}) FROM {}.{} WHERE {}').format(
            column == '*' and sql.SQL(column) or sql.Identifier(column),
            sql.Identifier(scheme),
            sql.Identifier(table),
            where)
        
        with Conn(self.__handle) as conn:
            with conn.cursor() as cur:
                cur.execute(cmd, values)
                print(cur.query)
                return cur.fetchone()['count']
 
    @valid_handler
    @exception_handler 
    def insert(self, scheme, table, row):
        cmd = sql.SQL('INSERT INTO {}.{} ({}) VALUES ({}) RETURNING *').format(
            sql.Identifier(scheme),
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, row.keys())),
            sql.SQL(', ').join(map(sql.Placeholder, row.keys()))
            )
        
        with Conn(self.__handle) as conn:
            with conn.cursor() as cur:
                cur.execute(cmd, row)
                print(cur.query)
                return cur.fetchone()
        
    @valid_handler
    @exception_handler
    def update(self, scheme, table, query, field):
        where, values = self.__where(query)
        cmd = sql.SQL('UPDATE {}.{} SET {} WHERE {} RETURNING *').format(
            sql.Identifier(scheme),
            sql.Identifier(table),
            sql.SQL(', ').join([sql.SQL('{}={}').format(sql.Identifier(k), sql.Placeholder(k)) for k in field.keys()]),
            where
            )
        
        values.update(field)
        with Conn(self.__handle) as conn:
            with conn.cursor() as cur:
                cur.execute(cmd, values)
                print(cur.query)
                return cur.fetchall()

    @valid_handler
    @exception_handler
    def delete(self, scheme, table, query):
        where, values = self.__where(query)
        cmd = sql.SQL('DELETE FROM {}.{} WHERE {}').format(
            sql.Identifier(scheme),
            sql.Identifier(table),
            where
            )

        with Conn(self.__handle) as conn:
            with conn.cursor() as cur:
                cur.execute(cmd, values)
                print(cur.query)
                return {'DELETE': cur.rowcount}

if __name__ == '__main__':
    handle = PGConnector(host='192.168.6.47', port=5433, user='silence', password='cd08taigu!', database='platform')

    query = {'AND': {'key1': 1, 'key2': [2,3], 'key3': {'>=': 10, '<': 20}, 'key4': [{'>': 5}, 3, 4]}, 
    'OR': {'key1': 1, 'key2': [2,3], 'key3': {'>=': 10, '<': 20}, 'key4': [{'>': 5}, 3, 4]},
    'NOT': {'AND': {'key1': 1, 'key2': [2,3], 'key3': {'>=': 10, '<': 20}, 'key4': [{'>': 5}, 3, 4]}, 
    'OR': {'key1': 1, 'key2': [2,3], 'key3': {'>=': 10, '<': 20}, 'key4': [{'>': 5}, 3, 4]}}}
    
    
    #query = {'NOT': {'OR': {'key1': 1, 'key2': [2,3], 'key3': {'>=': 10, '<': 20}, 'key4': [{'>': 5}, 3, 4]}}}

    data = handle.find('public', 'tokens', query, sort=[('f1', 'asc'),('f2', 'desc')])
    print(data)

#     for row in handle.find('public', 'tokens', {'id': [20, 21], 'user_id': 'cps11', 'issued_at': {'<=': '2018-10-23 01:36:33.150509', '>=': '2018-10-22 08:48:47.518051'}}, ['client_id', 'id'], {'issued_at': 'asc'}, 0, 10):
#         print(row)
    
    
    #data = handle.count('oauth', 'tokens', {'NOT': {'id': [20, 21], 'user_id': 'cps1111'}, 'YES': {'issued_at': {'<=': '2018-10-23 01:36:33.150509', '>=': '2018-10-22 08:48:47.518051'}}})
    #print(data)
    
#     data = handle.insert('test', 'test', {'a': 1, 'b': 2, 'c': 3})
#     print(data)

#     data = handle.update('test', 'test', {'id': [1,5], 'a': {'<=': '1'}}, {'c': 100})
#     print(data)

#     data = handle.delete('test', 'test', {'id': 100})
#     print(data)
