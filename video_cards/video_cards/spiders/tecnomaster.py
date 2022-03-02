from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
#from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

# Nombre pagina de producto  = $x('//div[@class="summary entry-summary"]/h1/text()').map(x=>x.wholeText)
# precio pagina de producto = $x('//div[@class="summary entry-summary"]/p[2]/text()').map(x=>x.wholeText)
# stock pagina de producto = $x('//span[@class="electro-stock-availability"]/p[@class="stock in-stock"]/text()').map(x=>x.wholeText)
# links de pagina de producto = $x('//link[@rel="canonical"]/@href').map(x=>x.value)

class productos(Item):
    nombre = Field()
    precios = Field()
    stock = Field()
    enlaces = Field()

class tecnomastercrawler(CrawlSpider):
    name = 'tecnomaster'

    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20, # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
      'FEED_EXPORT_FIELDS': ['nombre', 'precios', 'stock', 'enlaces'], # Como ordenar las columnas en el CSV?
    }

    allowed_domains = ['tecno-master.cl']

    start_urls = ['https://tecno-master.cl/categoria-producto/productos/hardware/tarjetasdevideo']

    #download_delay = 1

    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/paged\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
        Rule( # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/producto/' 
            ), follow=True, callback='parse_items'), # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )

    def parse_items(self, response):

            item = ItemLoader(productos(), response)
            
            # Utilizo Map Compose con funciones anonimas
            # PARA INVESTIGAR: Que son las funciones anonimas en Python?
            item.add_xpath('nombre', '//div[@class="summary entry-summary"]/h1/text()')
            item.add_xpath('precios', '//div[@class="summary entry-summary"]/p[2]/text()', MapCompose(lambda i: i.replace('.', '')))
            item.add_xpath('stock', '//span[@class="electro-stock-availability"]/p[@class="stock in-stock"]/text()')
            item.add_xpath('enlaces', '//link[@rel="canonical"]/@href')
            

            yield item.load_item()


process = CrawlerProcess({
    "FEEDS": {"/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/preproceso/tecnopre.csv": {"format": "csv", "overwrite": True}},
    'ROBOTSTXT_OBEY':'False',
    'USER_AGENT': 'Mozilla/5.0',



    #'AUTOTHROTTLE_ENABLED':'True',
    #'AUTOTHROTTLE_START_DELAY': '1'
    })

     #guardado de archivos
        

process.crawl(tecnomastercrawler)
process.start()