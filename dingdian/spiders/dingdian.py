import scrapy
import re
import string
from bs4 import BeautifulSoup
from scrapy.http import Request #单独的一个request模块，需要跟进url时候需要
from dingdian.items import DingdianItem,DcontentItem #导入字段对象
from dingdian.mysqlpipelines.sql import Sql
class Myspider(scrapy.Spider):
    name = 'dingdian'
    allowed_domains=['23wx.com']
    bash_url='http://www.23wx.com/class/'
    bashurl='.html'

    def start_requests(self):
        for i in range(1,11):
            url=self.bash_url+str(i)+'_1'+self.bashurl
            yield Request(url,self.parse)
    def parse(self, response):
        max_pagenum=BeautifulSoup(response.text,'lxml').find('a',class_='last').get_text()##作者不知道 这里有一个BUG
        bashurl=str(response.url)[:-7]
        for num in range(1,int(max_pagenum)+1):
            url=bashurl+'_'+str(num)+self.bashurl
            # print(url)
            yield Request(url,callback=self.get_name)
            '''yield request ,请求新的url,后面的是回调函数。你需要那个函数来处理这个数值就调用那个函数
            返回值以参数形式传递给你所调用的函数
            '''

    def get_name(self,response):
        tds=BeautifulSoup(response.text,'lxml').find_all('tr',bgcolor="#FFFFFF")
        for td in tds:
            novelname=td.find('td',class_="L").get_text()
            novelurl=td.find('a')['href']
            yield Request(novelurl,callback=self.get_chapterurl,meta={'name':novelname,'url':novelurl})

    def get_chapterurl(self,response):
        item=DingdianItem()
        item['name']=str(response.meta['name']).replace(string.whitespace,'')
        item['novelurl']=response.meta['url']
        category=BeautifulSoup(response.text,'lxml').find('table').find('a').get_text()
        author = BeautifulSoup(response.text, 'lxml').find('table').find_all('td')[1].get_text()
        bash_url = BeautifulSoup(response.text, 'lxml').find('p',class_="btnlinks").find('a',class_="read")['href']
        name_id = str(bash_url).split('/')[-2]
        item['category']=str(category).replace(string.whitespace,'')
        item['author'] = str(author).replace(string.whitespace,'')
        item['name_id'] = name_id
        # print(item)
        yield item
        yield Request(url=bash_url,callback=self.get_chapter,meta={'name_id':name_id})

    def get_chapter(self,response):
        urls=re.findall('<td class="L"><a href="(.*?)">(.*?)</a></td>',response.text)
        num=0
        for url in urls:
            num=num+1
            chapterurl=response.url+url[0]
            chaptername=url[1]
            rets=Sql.select_chapter(chapterurl)
            if rets[0]==1:
                print(u'章节已经存在了')
                return False
            else:
                yield Request(chapterurl,headers=headers,callback=self.get_chaptercontent,meta={'num':num,
                                                                                'name_id':response.meta['name_id'],
                                                                                'chaptername':chaptername,
                                                                                'chapterurl':chapterurl
                                                                                })
    def get_chaptercontent(self,response):
        item=DcontentItem()
        item['num']=response.meta['num']
        item['id_name']=response.meta['name_id']
        item['chaptername']=response.meta['chaptername']
        item['chapterurl'] = response.meta['chapterurl']
        content=BeautifulSoup(response.text,'lxml').find('dd',id="contents").get_text()
        item['chaptercontent']=str(content).replace(string.whitespace,'')
        # print(item)
        yield item
