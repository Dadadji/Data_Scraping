import scrapy
import numpy as np


class Tomato(scrapy.Spider):
    name = "Task_two"
    start_urls = [
        'https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/?page=1',
    ]

    def parse(self, response):
        i = np.arange(0, 96)

        for id in i:
            product = response.css('section.listing li#p'+str(id))

            yield {
                'Name': product.css('div.ellipsis p::text').get(),
                'Brand': product.css('span.productdesc a::attr(data-brand)').get(),
                'Price': product.css('span.price::text').get(),
                'Image URL':  "https:" + product.css('span.productimage img::attr(src)').get(),
                'Product URL': "https://www.blue-tomato.com" + product.css('span.productdesc a::attr(href)').get(),
            }

            next_page = response.css('section.filter li.next.browse a::attr(href)').get()

            if next_page is not None:
                next_page = "https://www.blue-tomato.com" + next_page
                yield scrapy.Request(url=next_page, callback=self.parse)