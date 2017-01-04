import random
from dingdian.settings import USER_AGENTS

class RandomUserAgent(object):
    '''
    这个类主要随机产生UA
    '''
    def __init__(self,agents):
        self.agents=USER_AGENTS

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler.setting.getlist('USER_AGENTS'))

    def process_request(self,request,spider):
        request.headers.setdault('User-Agent' , random.choice(self.agents))