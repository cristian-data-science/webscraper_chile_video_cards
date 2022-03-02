from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
#from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

# Nombre pagina de producto  = $x('//section[@id="mainContent"]//div[@class="titulo_marca"]//h1/text()').map(x=>x.wholeText)
# precio pagina de producto = $x('//div/h2[@itemprop="lowPrice"]/text()').map(x=>x.wholeText)
# stock pagina de producto = $x('//div[@id="stock-product"]//h3/text()').map(x=>x.wholeText)
# links de pagina de producto = $x('/html/head/meta[18]/@content').map(x=>x.value)

class productos(Item):
    nombre = Field()
    precios = Field()
    stock = Field()
    enlaces = Field()

class winpycrawler(CrawlSpider):
    name = 'autowinpy'

    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20, # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
      'FEED_EXPORT_FIELDS': ['nombre', 'precios', 'stock', 'enlaces'], # Como ordenar las columnas en el CSV?
    }

    allowed_domains = ['winpy.cl']

    start_urls = ['https://www.winpy.cl/partes-y-piezas/tarjetas-de-video/']

    #download_delay = 1

    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/paged/\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
        Rule( # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/venta/tarjeta-de-video' 
            ), follow=True, callback='parse_items'), # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )

    def parse_items(self, response):

            item = ItemLoader(productos(), response)
            
            # Utilizo Map Compose con funciones anonimas
            # PARA INVESTIGAR: Que son las funciones anonimas en Python?
            item.add_xpath('nombre', '//section[@id="mainContent"]//div[@class="titulo_marca"]//h1/text()', MapCompose(lambda i: i.replace('Tarjeta de Video ', '').replace('Tarjeta de video ', '').strip().upper()))
            item.add_xpath('precios', '//div/h2[@itemprop="lowPrice"]/text()')
            item.add_xpath('stock', '//div[@id="stock-product"]//h3/text()', MapCompose(lambda i: i.replace(' unidades en stock', '').replace(' unidad en stock', '').strip()))
            item.add_xpath('enlaces', '/html/head/meta[18]/@content')
            

            yield item.load_item()


process = CrawlerProcess({
    "FEEDS": {"/home/ubuntu/gitprojects/webscraper_chile_video_cards/video_cards/video_cards/resultados/wpfinal.csv": {"format": "csv", "overwrite": True}},
    'ROBOTSTXT_OBEY':'False',
    'USER_AGENT': 'Mozilla/5.0',



    #'AUTOTHROTTLE_ENABLED':'True',
    #'AUTOTHROTTLE_START_DELAY': '1'
    })

     #guardado de archivos
        

process.crawl(winpycrawler)
process.start()