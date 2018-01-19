#-*- coding:utf-8 -*-
from time import sleep
import unittest,random,sys
import sys
sys.path.append(".\models")
sys.path.append(".\page_obj")
from models import myunit,function
from models.getconfigs import GetConfigs
from page_obj.searchPage import serachPage
from models.log import log


class search_box(myunit.MyTest):
    logger = log()
    GET = GetConfigs()
    name1 = GET.getstr('Login', 'world1', 'common', exc=None)
    name2 = GET.getstr('Login', 'world2', 'common',exc=None)

    def search_text(self,word=''):
        serachPage(self.driver).search_idea(word)

    def test_search1(self):
        '''搜索结果为空'''
        try:
            self.search_text(word=self.name1)
            sleep(10)
            s = serachPage(self.driver)
            self.assertNotEqual(s.count_idea(), u"魅族社区")
        except Exception, e:
            function.insert_img(self.driver, 'bbs0.png')
            self.logger.error(u"对不起，我没有找到匹配结果。")
            raise e

    def test_search2(self):
        '''搜索结果不为空'''
        try:
            self.search_text(word=self.name2)
            s = serachPage(self.driver)
            self.assertEqual(s.count_idea(),u"魅族社区")
        except Exception, e:
            function.insert_img(self.driver,'bbs1.png')
            self.logger.error(u'判断语句出错')
            raise e


if __name__ == "__main__":
    unittest.main()
