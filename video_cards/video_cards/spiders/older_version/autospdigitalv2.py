from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
#from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

# Nombre pagina de producto  = $x('//div[@class="product-detail-module--titleContainer--FjMOA"]/div[@data-fractalds="t:a|n:typography|v:subtitle,default,left,div"]/text()').map(x=>x.wholeText)
# precio pagina de producto = $x('//div[@class="product-detail-module--payments--vheAN"]//span[@data-fractalds="t:a|n:typography|v:best-price-sm,primary,left,span"]/text()').map(x=>x.wholeText)
# stock pagina de producto = $x('//div[@class="product-detail-module--payments--vheAN"]/div[@class="Fractal-Typography--base Fractal-Typography--typographyBodySm Fractal-Typography__typography--default   Fractal-Typography__typography--left product-detail-module--availability--RASQg product-detail-module--successText--41yYx"]//text()[1]').map(x=>x.wholeText)
# links de pagina de producto = $x('/html/head/script[6]/text()[1]').map(x=>x.wholeText)

class productos(Item):
    nombre = Field()
    precios = Field()
    stock = Field()
    enlaces = Field()

class spdigitalv2crawler(CrawlSpider):
    name = 'autospdigitalv2'

    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20, # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
      'FEED_EXPORT_FIELDS': ['nombre', 'precios', 'stock', 'enlaces'], # Como ordenar las columnas en el CSV?
    }

    allowed_domains = ['spdigital.cl']

    start_urls = ['https://www.spdigital.cl/categories/componentes-tarjeta-de-video/']

    download_delay = 1

    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
        Rule( # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/componentes-tarjeta-de-video/' 
            ), follow=True, callback='parse_items'), # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )

    def parse_items(self, response):

            item = ItemLoader(productos(), response)
            
            # Utilizo Map Compose con funciones anonimas
            # PARA INVESTIGAR: Que son las funciones anonimas en Python?
            item.add_xpath('nombre', '//div[@class="product-detail-module--titleContainer--FjMOA"]/div[@data-fractalds="t:a|n:typography|v:subtitle,default,left,div"]/text()')
            item.add_xpath('precios', '//div/h2[@itemprop="lowPrice"]/text()')
            item.add_xpath('enlaces', '/html/head/script[6]/text()[1]')
            item.add_xpath('stock', '//div[@class="product-detail-module--payments--vheAN"]/div[@class="Fractal-Typography--base Fractal-Typography--typographyBodySm Fractal-Typography__typography--default   Fractal-Typography__typography--left product-detail-module--availability--RASQg product-detail-module--successText--41yYx"]//text()[1]')
            

            yield item.load_item()


process = CrawlerProcess({
    "FEEDS": {"/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/TESTSP.csv": {"format": "csv", "overwrite": True}},
    'ROBOTSTXT_OBEY':'False',
    'USER_AGENT': 'Mozilla/5.0',



    #'AUTOTHROTTLE_ENABLED':'True',
    #'AUTOTHROTTLE_START_DELAY': '1'
    })

     #guardado de archivos
        

process.crawl(spdigitalv2crawler)
process.start()