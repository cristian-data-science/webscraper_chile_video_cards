from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
#from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

# categorería tarjetas de video = https://www.pcfactory.cl/tarjetas-graficas?categoria=334&papa=633&pagina=1
# xpath nombr_p_pcfactory = $x('//div[@class="p-relative"]/div/text()').map(x=>x.wholeText)
# xpath precios_pcfactory = $x('//div[@class="product__price-texts"]/div[@class="title-md color-primary-1"]/text()').map(x=>x.wholeText)
# xpath stock_pcfactory = $x('//div[@class="product__units"]/p/text()').map(x=>x.wholeText)
# xpath pagina_siguiente_pcfactory = $x('//div[@class="product__image"]/a/@href').map(x=>x.value)


    
    
class videoSpider(Spider):
    name = 'pcfactory'
    start_urls = [
        "https://www.pcfactory.cl/tarjetas-graficas?categoria=334&papa=633&pagina=1",
        "https://www.pcfactory.cl/tarjetas-graficas?categoria=334&papa=633&pagina=2"       
    ]

    def parse(self, response):
        nombre_p = response.xpath('//div[@class="p-relative"]/div/text()').getall()
        precio_p = response.xpath('//div[@class="product__price-texts"]/div[@class="title-md color-primary-1"]/text()').getall()
        stock_p = response.xpath('//div[@class="product__units"]/p/text()').getall()
        links_p = response.xpath('//div[@class="product__image"]/a/@href').getall()

        yield {
            "nombre_p": nombre_p, 
            "precios_p": precio_p,
            "stock_p" : stock_p,
            "links_p" : links_p 
        }

process = CrawlerProcess({
    "FEEDS": {"./video_cards/video_cards/preproceso/pc_pre.csv": {"format": "csv", "overwrite": True}},
    'ROBOTSTXT_OBEY':'False',
    'USER_AGENT': 'Mozilla/5.0',



    #'AUTOTHROTTLE_ENABLED':'True',
    #'AUTOTHROTTLE_START_DELAY': '1'
    })

     #guardado de archivos
        

process.crawl(videoSpider)
process.start()