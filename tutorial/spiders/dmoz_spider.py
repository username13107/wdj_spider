# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import DmozItem
import re
import os
from selenium import webdriver
from scrapy.selector import HtmlXPathSelector, Selector
import time
import urllib

class DmozSpiderSpider(scrapy.Spider):
    name = "dmoz_spider"
    allowed_domains = ["wandoujia.com"]
    start_urls = (
        ##排行###
        #"http://www.wandoujia.com/top/app",
        #"http://www.wandoujia.com/top/game"
        ##分类###
        # "http://www.wandoujia.com/tag/影音图像",#影音图像
        # "http://www.wandoujia.com/tag/通信聊天",#通信聊天
        # "http://www.wandoujia.com/tag/网上购物",#网上购物
        # "http://www.wandoujia.com/tag/美化手机",#美化手机
        # "http://www.wandoujia.com/tag/阅读学习",#阅读学习
        # "http://www.wandoujia.com/tag/便捷生活",#便捷生活
        # "http://www.wandoujia.com/tag/常用工具",#常用工具
        # "http://www.wandoujia.com/tag/出行必用",#出行必用
        # "http://www.wandoujia.com/tag/性能优化",#性能优化
        #"http://www.wandoujia.com/tag/新闻资讯", #新闻资讯
        # "http://www.wandoujia.com/tag/社交网络",#社交网络
        # "http://www.wandoujia.com/tag/金融理财",#金融理财
        # "http://www.wandoujia.com/tag/办公软件",#办公软件
        # "http://www.wandoujia.com/tag/育儿母婴",#育儿母婴

        ###照片##
        # "http://www.wandoujia.com/tag/相册",
        # "http://www.wandoujia.com/tag/滤镜",
        # "http://www.wandoujia.com/tag/相机",

        ###影音
        "http://www.wandoujia.com/tag/视频",
        # "http://www.wandoujia.com/tag/播放器",
        # "http://www.wandoujia.com/tag/音乐",


        #游戏#
        # "http://www.wandoujia.com/tag/休闲时间",
        # "http://www.wandoujia.com/tag/跑酷竞速",
        # "http://www.wandoujia.com/tag/宝石消除",
        # "http://www.wandoujia.com/tag/网络游戏",
        # "http://www.wandoujia.com/tag/动作射击",
        # "http://www.wandoujia.com/tag/扑克棋牌",
        # "http://www.wandoujia.com/tag/儿童益智",
        # "http://www.wandoujia.com/tag/塔防守卫",
        # "http://www.wandoujia.com/tag/体育格斗",
        # "http://www.wandoujia.com/tag/角色扮演",
        # "http://www.wandoujia.com/tag/经营策略",
    )

    def parse_top(self, response):
      filename = "top_" + response.url.split('/')[-1]
      f = open(filename, "w")
      rx1 = ur"<li data-pn=\"(.*?)\" class=\"(.*?)\""
      rx2 = ur"<li class=\"(.*?)\" data-pn=\"(.*?)\""
      driver = webdriver.Chrome(os.environ['webdriver.chrome.driver'])
      driver.get(response.url)
      for i in range(1, 100):
        try:
          driver.find_element_by_id("j-refresh-btn").click() 
          time.sleep(2)
        except:
          break
      sou=driver.page_source
      #hxs = HtmlXPathSelector(text=sou2)
      cnt = 0
      hxs = Selector(text=sou)
      for sel in hxs.xpath('//*[@id="j-top-list"]/li'):
        cnt += 1
        #print sel
        item = DmozItem()
        item['cls'] = sel.xpath('a[@class="tag-link"]/text()').extract()
        item['isc'] = sel.xpath('div[@class="app-desc"]/div[@class="meta"]/span[@class="install-count"]/text()').extract()[0]
        print "install count ", item['isc']
        ma1 = re.search(rx1, sel.extract())
        ma2 = re.search(rx2, sel.extract())
        
        if ma1:
          item['pn'] = ma1.group(1)
          #print item['pn'], " | ", item['cls'][0]
          data = u' '.join((item['pn'], item['cls'][0])).encode('utf-8').strip()
          #print data
          f.write(data)
          f.write(u'\n')
        elif ma2:
          item['pn'] = ma2.group(2)
          #print item['pn'], " | ", item['cls'][0]
          data = u' '.join((item['pn'], item['cls'][0])).encode('utf-8').strip()
          #print data
          f.write(data)
          f.write(u'\n')
        else:
          #print 'not found!'
          continue
  
      data = u"total found %d packages\n" % cnt
      f.write(data)
      driver.close()

    def parse_tag(self, response):
      # print response.url
      urllk = urllib.unquote(response.url.replace("\\x","%"))
      clsname = urllk.split('/')[-1]
      filename = "tag_app_" + clsname
      f = open(filename, "w")
      rx1 = ur"data-install=\"(.*?)\".*data-name=\"(.*?)\".*data-pn=\"(.*?)\""
      rx2 = ur"<li class=\"(.*?)\" data-pn=\"(.*?)\""
      driver = webdriver.Chrome(os.environ['webdriver.chrome.driver'])
      driver.get(response.url)
      for i in range(1, 100):
        try:
          driver.find_element_by_id("j-refresh-btn").click() 
          time.sleep(1)
        except:
          break
      sou=driver.page_source
      cnt = 0
      name = ""
      hxs = Selector(text=sou)
      for sel in hxs.xpath('//*[@id="j-tag-list"]/li'):
        item = DmozItem()
        item['cls'] = clsname
        print sel
        try:
          if len(sel.xpath('a[@class="install-btn"]').extract()) > 0:
            ma1 = re.search(rx1, sel.xpath('a[@class="install-btn"]').extract()[0])
          elif len(sel.xpath('a[@class="install-btn "]').extract()) > 0:
            ma1 = re.search(rx1, sel.xpath('a[@class="install-btn "]').extract()[0])
          else:
            continue

          if ma1:
            cnt += 1
            #print "install:",ma1.group(1), "name:", ma1.group(2), " pn:", ma1.group(3)
            item['pn'] = ma1.group(3)
            item['isc'] = ma1.group(1)
            name = ma1.group(2)
            #print item['pn'], " | ", item['cls'][0]
            data = u' '.join((item['pn'], item['isc'])).encode('utf-8').strip()
            #print data
            f.write(data)
            f.write(u'\n')
          else:
            print 'not found!'
            continue
        except:
          continue
  
      data = u"total found %d packages\n" % cnt
      print "cate:", clsname, " total:", data, "last app:", name
      f.write(data)
      driver.close()


    def parse(self, response):
      which = 0
      try:
        if response.url.index('top') > 0:
          which = 1
      except:
        which = 0

      if which == 1:
        self.parse_top(response)
      else:
        self.parse_tag(response)
      
