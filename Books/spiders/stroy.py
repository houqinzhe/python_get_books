import scrapy
from Books.items import BooksItem


class StroySpider(scrapy.Spider):
    name = 'stroy'
    start_urls = ['https://www.biquge9.cc/book/18220312/672306968.html']

    def parse(self, response):
        item = BooksItem()
        def text_to_string(list):
            # s = str(list)
            # p = r'[\u4e00-\u9fa5]+|[，]+|[。]' # 匹配汉字，逗号
            # r = re.findall(p, s)
            return ''.join(list)
        item['section'] = response.css('div.content h1::text').get()
        item['text_info'] = response.css('div.textinfo span::text').getall()
        item['content'] = text_to_string(response.css('div.showtxt::text').getall())
        next_section = response.css('div.page_chapter a::attr(href)').getall()[2]

        yield item
        # with open('aa.txt', 'w') as f: # 这样写入会一直打开关闭 覆盖之前的内容 是不可取的， 可能要在管道里边操作
        #   f.write(section)
        #   f.write(content)

        if next_section is not None:
            yield scrapy.Request(next_section, callback=self.parse)


