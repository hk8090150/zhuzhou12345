# -*- coding: utf-8 -*-
import scrapy
from scrapy import Field
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zhuzhou12345.items import Zhuzhou12345Item
import re



class ZhuzhouSpider(CrawlSpider):
    name = "zhuzhou"

    allowed_domains = ["zhuzhou.gov.cn"]
    url = 'http://12345.zhuzhou.gov.cn:8066/12345/front/email.do?method=query&pageIndex='
    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        # 取出每个页面里帖子链接列表
        url2 = 'http://12345.zhuzhou.gov.cn:8066/12345/front/email.do?method=querymail&action=view&id='
        page_linke=response.xpath('//td[@class="f5"][3]/a').re("onclick=.*?(\d+)")

        for node in page_linke:
            node=[url2 + str(node)]
            yield scrapy.Request(node[0], callback=self.parse_item)


        if self.offset <= 810:
            self.offset += 1

            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def parse_item(self, response):
        item = Zhuzhou12345Item()
        # print(response.url)


        # 信件标题
        item["Letter"] = response.xpath(r'//tbody/tr[1]/td[@class="bf18"]/text()').extract()[0].strip()
        # 来信内容
        LetterContent = response.xpath(r'//td/table/tbody/tr[2]/td/p/text()').extract()[0].strip()
        item["LetterContent"] = re.sub(r'\s+', '', LetterContent)
        ##来信时间
        LetterTime = response.xpath(r"//tbody/tr[3]/td/div/p/text()").extract()[1].strip()
        item["LetterTime"] = LetterTime.replace("写信时间：", "").strip()
        #来信人
        LetterName = response.xpath(r"//tbody/tr[3]/td/div/p/text()").extract()[0].strip()
        item["LetterName"] = LetterName.replace("写信人：", "").strip()



        # # 来信答复
        # ReplyLetter = response.xpath(r'//td/div[@class="huifu"]/p[2]/text()').extract()[0].strip()
        # if len(ReplyLetter)==0:
        #     ReplyLetter = response.xpath(r'//tbody/tr[2]/td/table/tbody/tr[2]/td/div').extract()[0].strip()
        #     item["ReplyLetter"] = re.sub(r'\s+', '', ReplyLetter)

        ## 来信答复
        item["ReplyLetter"] = self.get_ReplyLetter(response)
        # 回信时间
        item["ReplyTime"] = self.get_ReplyTime(response)
        #回信者单位或名字
        item["Responders"] = self.get_Responders(response)




        # ReplyTime = response.xpath(r"//td/div[@class='huifu']/p[4]/text()").extract()[0].strip()

        #
        # if len(ReplyTime) == 21:
        #     item["ReplyTime"] =ReplyTime
        # ReplyTime = response.xpath(r'//tr[2]/td/div[@class="huifu"]/p[9]/font/text()').extract()[0].strip()





        # # 回信者单位或名字
        # Responders = response.xpath("//td/div[@class='huifu']/p[3]/text()").extract()[0].strip()
        # if len(Responders)!=0:
        #     item["Responders"]=Responders

        # 详细url连接网址
        item["url"] = response.url
        yield item

    # 来信答复
    def get_ReplyLetter(self, response):
        ReplyLetter1 = response.xpath('//td/table/tbody/tr[2]/td/div/p[3]/span/font/text()')
        ReplyLetter2 = response.xpath(r'//tr[2]/td/div[@class="huifu"]/p/font/text()').extract()
        ReplyLetter3 = response.xpath(r'//td/div[@class="huifu"]/p[2]/text()').extract()[0].strip()
        ReplyLetter4 = response.xpath(r'//tbody/tr[2]/td/div/p[(@class="MsoNormal")]/span/text()').extract()
        ReplyLetter5 = response.xpath(r'//table/tbody/tr[2]/td/table/tbody/tr[2]/td/div/p/text()').extract()
        if len(ReplyLetter1):
            ReplyLetter = re.sub(r'\s+', '', ReplyLetter1.extract_first().strip())
        elif ReplyLetter2:
            ReplyLetter =  re.sub(r'\s+', '',("".join(ReplyLetter2)))
        elif ReplyLetter3:
            ReplyLetter = re.sub(r'\s+', '', (ReplyLetter3)).strip()
        elif ReplyLetter4:
            ReplyLetter = "".join(ReplyLetter4)
        elif ReplyLetter5:
            ReplyLetter = re.sub(r'\s+', '',("".join(ReplyLetter5)))
        else:
            ReplyLetter = ""
        return ReplyLetter.strip()

    # 回信时间
    def get_ReplyTime(self, response):
        ReplyTime = response.xpath(r"//td/div[@class='huifu']/p[4]/text()").extract_first()
        pattern = re.compile((r"\d{4}(\-|\/|.)\d{1,2}\1\d{1,2}\s\d{2}(\-|)(\:|)\d.(\:)\d{2}"))
        ReplyTime= pattern.search(str(ReplyTime))
        ReplyTime1 = response.xpath(r'//td/div[@class="huifu"]/p[8]/font/text()').extract_first()
        ReplyTime2 = response.xpath(r'//tbody/tr[2]/td/div[@class="huifu"]/p[7]/font/text()').extract_first()
        ReplyTime3 = response.xpath(r'//tbody/tr[2]/td/div[@class="huifu"]/p[4]/text()').extract_first()


        if (ReplyTime is not None  ):
            print("**"*60)
            print(ReplyTime[0] )
            ReplyTime =  ReplyTime[0].strip()

        #     print("**" * 60)
        elif ReplyTime1:
            ReplyTime=ReplyTime1.strip()
        elif ReplyTime2:
            ReplyTime = ReplyTime2.strip()
        elif ReplyTime3:
            ReplyTime = ReplyTime3.strip()
        else:
            ReplyTime = ""
        return ReplyTime
        # 回信者单位或名字
    def get_Responders(self, response):
        Responders = response.xpath("//td/div[@class='huifu']/p[3]/text()").extract()
        if len(Responders):
            Responders = "".join(Responders)[0:10].strip()
        else:
            Responders = ""
        return Responders.strip()










        #     each.url = each.url.replace("?", "&").replace("Type&", "Type?")
        # return links

    # def parse_item(self, response):
    #     # item = NewdongguanItem()
    #     pass




    #
    # rules = (
    #     # 提取匹配 'pageIndex=2/' (但不匹配 'subsection.php') 的链接并跟进链接(没有callback意味着follow默认为True)
    #     Rule(LinkExtractor(allow=r'method=query&pageIndex=\d+'), callback='parse_item', follow=True),
    #     # 提取匹配 'item.php' 的链接并使用spider的parse_item方法进行分析
    #     Rule(LinkExtractor(allow=('item\.php',)), callback='parse_item'),
    # )

    # rules = (
    #     Rule(LinkExtractor(allow=r'method=query&pageIndex=\d+'), follow=True),
    #     Rule(LinkExtractor(allow=(r'/item/*')), follow=False, callback="parse_item"),
    # )


    # def parse_item(self, response):
    #     item = Zhuzhou12345Item()
    #     for node in LinkExtractor(restrict_xpaths='//td[@class="f5"][3]'):
    #         # 信件类别
    #         item["Consulting"] = node.xpath("//tbody/tr[2]/td[@class='f5'][2]/text()").extract()[0].strip()
    #         item["Letter"] = node.xpath("./[3]/a/text()").extract()[0].strip()  # 信件标题
    #         item["ClickCount"] = node.xpath("./td[7]/text()").extract()[0].strip()  # 点击次数
    #         item["NameLetter"] = node.xpath("./td[2]/a/text()").extract()[0].strip()  # 来信人名字
    #         item["LetterTime"] = node.xpath("./td[4]/text()").extract()[0].strip()  # 来信时间
    #         item["LetterContent"] = node.xpath("./td[7]/text()").extract()[0].strip()  # 来信内容
    #         item["ReplyLetter"] = node.xpath("./td[2]/a/text()").extract()[0].strip()  # 来信答复
    #         item["Responders"] = node.xpath("./td[4]/text()").extract()[0].strip()  # 回信者
    #         item["ReplyTime"] = node.xpath("//td/div[@class='huifu']/p[4]/text()).extract()[0].strip()  # 回信时间
    #         item["url"] = node.xpath("./td[7]/text()").extract()[0].strip()  # 回信时间
    #
    #         yield item

