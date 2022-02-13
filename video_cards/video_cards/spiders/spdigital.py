import scrapy

# xpath nombres_productos = $x('//*[@id="grid"]/div[2]/div/div//a/span/@data-original-title').map(x=>x.value)
# xpath precios = $x('//div/div[@class="span2 product-item-mosaic"]/div[@class="cash-price"]/text()').map(x=>x.wholeText)
# xpath stock = $x('//*[@id="grid"]/div[2]/div/div/div[6]/text()').map(x=>x.wholeText)
# xpath next_page = $x('//div[@class="pagination"]/ul/li/a[@class="next"]/@href').map(x=>x.value)
# xpath link = $x('//div[@class="span2 product-item-mosaic"]/div[@class="image"]/a/@href').map(x=>x.value)

custom_settings = {
        'CURRENT_REQUESTS': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['cgutierrez.infor@gmail.com'],
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    
class videoSpider(scrapy.Spider):
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