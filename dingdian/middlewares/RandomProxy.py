import random
import pandas as pd
from sqlalchemy import create_engine
from dingdian import settings
from jiandan.db.db_helper import DB_Helper##这里要好好修改

'''
这个类主要产生随机的IP
'''
class RandomProxy(object):
    def __init__(self):
        self.db_helper=DB_helper()
        self.count=self.db_helper.proxy.count()
    def process_request(self,request,spider):
        '''
        在请求上添加代理
        ：:param request
        :param spider
        :return
        '''
        dbfile = r'/home/rising/Program/IPProxyPool/IPProxyPool_py3/data/proxy.db'
        db_conn = create_engine('sqlite:///' + dbfile)
        df = pd.read_sql('select * from proxys', db_conn)
        df.update(df.port.map(str))
        iplist = list('http://' + df.ip + ':' + df.port)
        ip = random.choice(iplist)
        # result = self.db_helper.findOneResult({'proxyId':ip})
        request.meta['proxy'] =ip
