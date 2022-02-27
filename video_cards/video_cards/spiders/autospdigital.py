from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
#from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

# xpath nombres_productos = $x('//*[@id="grid"]/div[2]/div/div//a/span/@data-original-title').map(x=>x.value)
# xpath precios = $x('//div/div[@class="span2 product-item-mosaic"]/div[@class="cash-price"]/text()').map(x=>x.wholeText)
# xpath stock = $x('//*[@id="grid"]/div[2]/div/div/div[6]/text()').map(x=>x.wholeText)
# xpath next_page = $x('//div[@class="pagination"]/ul/li/a[@class="next"]/@href').map(x=>x.value)
# xpath link = $x('//div[@class="span2 product-item-mosaic"]/div[@class="image"]/a/@href').map(x=>x.value)

custom_settings = {
        'FEED_URI': 'spfinal.json',
        'CURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'FEED_FORMAT': 'json',
        'MEMUSAGE_NOTIFY_MAIL': ['cgutierrez.infor@gmail.com'],
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/74.0.3729.169 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    
class videoSpider(Spider):
    name = 'spdigital'
    start_urls = [
        'https://www.spdigital.cl/categories/view/379/page:1'
    ]

    def parse_nextpages(self, response, **kwargs):
        if kwargs:
            nombre_sp = kwargs['nombre_sp']
            precios_sp = kwargs['precios_sp']
            stock_sp = kwargs['stock_sp']
            links_sp = kwargs['links_sp']

        nombre_sp.extend(response.xpath('//*[@id="grid"]/div[2]/div/div//a/span/@data-original-title').getall())
        precios_sp.extend(response.xpath('//div/div[@class="span2 product-item-mosaic"]/div[@class="cash-price"]/text()').getall())
        stock_sp.extend(response.xpath('//*[@id="grid"]/div[2]/div/div/div[6]/text()').getall())
        links_sp.extend(response.xpath('//div[@class="span2 product-item-mosaic"]/div[@class="image"]/a/@href').getall())

        next_page_button_link = response.xpath('//div[@class="pagination"]/ul/li/a[@class="next"]/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_nextpages, cb_kwargs={'nombre_sp': nombre_sp, 'precios_sp': precios_sp, 'stock_sp': stock_sp, 'links_sp': links_sp})
        else:
            yield{
                'nombre_sp': nombre_sp,
                'precios_sp': precios_sp,
                'stock_sp' : stock_sp,
                'links_sp' : links_sp
            }

    def parse(self, response):

        nombre_sp = response.xpath('//*[@id="grid"]/div[2]/div/div//a/span/@data-original-title').getall()
        precios_sp = response.xpath('//div/div[@class="span2 product-item-mosaic"]/div[@class="cash-price"]/text()').getall()
        stock_sp = response.xpath('//*[@id="grid"]/div[2]/div/div/div[6]/text()').getall()
        links_sp = response.xpath('//div[@class="span2 product-item-mosaic"]/div[@class="image"]/a/@href').getall()



        next_page_button_link = response.xpath('//div[@class="pagination"]/ul/li/a[@class="next"]/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_nextpages, cb_kwargs={'nombre_sp': nombre_sp, 'precios_sp': precios_sp, 'stock_sp': stock_sp, 'links_sp': links_sp})


process = CrawlerProcess({
    "FEEDS": {"/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/sp_pre.json": {"format": "json", "overwrite": True}},
    'ROBOTSTXT_OBEY':'False',
    'USER_AGENT': 'Mozilla/5.0',



    #'AUTOTHROTTLE_ENABLED':'True',
    #'AUTOTHROTTLE_START_DELAY': '1'
    })

     #guardado de archivos
        

process.crawl(videoSpider)
process.start()