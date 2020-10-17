import scrapy
#import numpy as np


class task_one(scrapy.Spider):
    name = 'product'
    page_number = 2
    start_urls = {
        #'https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx'
        'https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page=1&view=180&scale=282'
    }

    def _parse(self, response):

        for data in response.css('a._5ce6f6' ):
            yield{
                'name': data.css('p::text').get(),
                'brand name': data.css('h3::text').get(),
                'price': data.css('div._6356bb span::text').get(),
                'imageLink': data.css('meta::attr(content)').get(),
                'productLink': "https://farfetch.com" + data.css('a._5ce6f6::attr(href)').get(),

            }

        next_page = 'https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page='+str(task_one.page_number)+ '&view=180&scale=282'
        if task_one.page_number < 86:
            task_one.page_number +=1
            yield scrapy.Request(next_page, callback=self.parse)




            #next_page = response.css('div._5fd441 _d78341 a::attr(href)').get()
            #if next_page is not None:
            #    next_page = "https://www.farfetch.com" + next_page
            #    yield scrapy.Request(url=next_page, callback=self.parse)
        #next_page = 'https://www.farfetch.com/de/shopping/men/shoes-2/items.aspx?page='+ str(task_one.page_number)+'&view=180&scale=282'
        #if task_one.page_number < 89:
        #    task_one.page_number +=1
        #    yield scrapy.Request(url=next_page, callback=self.parse)