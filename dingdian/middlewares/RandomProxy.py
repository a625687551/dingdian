import random
import requests
import json
import pandas as pd
from sqlalchemy import create_engine
from dingdian import settings

'''
这个类主要产生随机的IP
'''


class RandomProxy(object):
    def __init__(self):
        '''
                初始化IP pool
        '''
        # dbfile = r'/home/rising/Program/IPProxyPool/IPProxyPool_py3/data/proxy.db'
        # db_conn = create_engine('sqlite:///' + dbfile)
        # df = pd.read_sql('select * from proxys', db_conn)
        # df.update(df.port.map(str))
        # self.iplist = list('http://' + df.ip + ':' + df.port)
        self.iplist = []
        r = requests.get(url='http://127.0.0.1:8000/?count=30&country=国内')
        ip_ports = json.loads(r.text)
        # for i in ip_ports:
        #     self.iplist.append('http://'+re.sub('\n','',i).strip())
        for i in ip_ports:
            self.iplist.append('http://' + str(i[0]) + ':' + str(i[1]))

    def process_request(self, request, spider):
        '''
        在请求上添加代理
        '''

        ip = random.choice(self.iplist)
        # result = self.db_helper.findOneResult({'proxyId':ip})
        request.meta['proxy'] = ip

    def process_response(self, request, response, spider):
        '''
        检查response.status, 根据status是否在允许的状态码中决定是否切换到下一个proxy, 或者禁用proxy
        '''
        if response.status != 200:
            new_request = request.copy()
            new_request.dont_filter = True
            print(u'更换代理')
            return new_request
        else:
            return response
