import scrapy

# categorería tarjetas de video = https://www.pcfactory.cl/tarjetas-graficas?categoria=334&papa=633&pagina=1
# xpath nombr_p_pcfactory = $x('//div[@class="p-relative"]/div/text()').map(x=>x.wholeText)
# xpath precios_pcfactory = $x('//div[@class="product__price-texts"]/div[@class="title-md color-primary-1"]/text()').map(x=>x.wholeText)
# xpath stock_pcfactory = $x('//div[@class="product__units"]/p/text()').map(x=>x.wholeText)
# xpath pagina_siguiente_pcfactory = $x('//*[@id="app"]/div[5]/div/div[1]/div/div[2]/div[6]/div[2]/a/@href').map(x=>x.value)

custom_settings = {
        'CURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['cgutierrez.infor@gmail.com'],
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    
class videoSpider(scrapy.Spider):
    name = 'pcfactory'
    start_urls = [
        'https://www.pcfactory.cl/tarjetas-graficas?categoria=334&papa=633&pagina=1',
        'https://www.pcfactory.cl/tarjetas-graficas?categoria=334&papa=633&pagina=2'       
    ]


    def parse(self, response):
        nombre_p = response.xpath('//div[@class="p-relative"]/div/text()').getall()
        precio_p = response.xpath('//div[@class="product__price-texts"]/div[@class="title-md color-primary-1"]/text()').getall()
        stock_p = response.xpath('//div[@class="product__units"]/p/text()').getall()

        yield {
            "nombre_p": nombre_p, 
            "precios_p": precio_p,
            "stock_p" : stock_p
        }