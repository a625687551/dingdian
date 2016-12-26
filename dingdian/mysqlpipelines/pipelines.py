from .sql import Sql
from dingdian.items import DingdianItem,DcontentItem

class DingdianPipeline(object):

    def process_item(self,item,spider):
        if isinstance(item,DingdianItem):
            name_id=item['name_id']
            ret=Sql.select_name(name_id)
            if ret[0]==1:
                print(u'{}已经存在了'.format(name_id))
                pass
            else:
                xs_name=item['name']
                xs_author=item['author']
                category=item['category']
                Sql.insert_dd_name(xs_name,xs_author,category,name_id)
                print(u'开始存小说标题')

        if isinstance(item,DcontentItem):
            url = item['chapterurl']
            name_id = item['chapterurl']
            num_id = item['chapterurl']
            xs_chaptername = item['chapterurl']
            xs_content = item['chapterurl']
            Sql.insert_dd_chaptername(xs_chaptername,xs_content,name_id,num_id,url)
            print(u'{}章节存入完毕'.format(xs_chaptername))
            return item